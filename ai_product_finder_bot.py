import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def extract_price(text):
    text = text.replace(',', '').replace('₹', '').strip()
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None

def search_flipkart(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = query.replace(' ', '+')
    url = f"https://www.flipkart.com/search?q={query}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = []
    for item in soup.find_all('div', {'class': '_1AtVbE'}):
        name_tag = item.find('a', {'class': 'IRpwTa'}) or item.find('a', {'class': 's1Q9rs'})
        price_tag = item.find('div', {'class': '_30jeq3'})
        link_tag = item.find('a', href=True)
        if name_tag and price_tag and link_tag:
            name = name_tag.text.strip()
            price = extract_price(price_tag.text)
            link = "https://www.flipkart.com" + link_tag['href']
            results.append({'name': name, 'price': price, 'link': link})
            if len(results) >= 5:
                break
    return results

def search_amazon(query):
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}
    query = query.replace(' ', '+')
    url = f"https://www.amazon.in/s?k={query}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = []
    for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
        name_tag = item.find('span', {'class': 'a-text-normal'})
        price_whole = item.find('span', {'class': 'a-price-whole'})
        price_fraction = item.find('span', {'class': 'a-price-fraction'})
        link_tag = item.find('a', {'class': 'a-link-normal'}, href=True)
        if name_tag and price_whole and link_tag:
            name = name_tag.text.strip()
            price_text = price_whole.text + (price_fraction.text if price_fraction else '')
            price = extract_price(price_text)
            link = "https://www.amazon.in" + link_tag['href']
            results.append({'name': name, 'price': price, 'link': link})
            if len(results) >= 5:
                break
    return results

def filter_results(results, max_price, keywords):
    filtered = []
    for r in results:
        if r['price'] and r['price'] <= max_price:
            if all(k.lower() in r['name'].lower() for k in keywords):
                filtered.append(r)
    return filtered

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to your AI Product Finder Bot!\n\nSend your product requirements and max budget like:\n'laptop Ryzen 7 16GB under 55000'\n\nI will fetch and send you the best options available online.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    match = re.search(r'(.*) under (\d+)', user_input)
    if not match:
        await update.message.reply_text("❌ Please send in the format: 'product specs under 55000'")
        return
    query = match.group(1).strip()
    max_price = int(match.group(2))
    keywords = query.split()
    await update.message.reply_text("🔍 Searching the best products for you, please wait...")
    fk_results = search_flipkart(query)
    amz_results = search_amazon(query)
    combined = fk_results + amz_results
    filtered = filter_results(combined, max_price, keywords)
    if not filtered:
        await update.message.reply_text("No matching products found. Try adjusting your budget or keywords.")
        return
    filtered.sort(key=lambda x: x['price'])
    reply_text = "Here are the top options I found:\n\n"
    for idx, r in enumerate(filtered[:5], 1):
        reply_text += f"{idx}. {r['name']}\n₹{r['price']}\n{r['link']}\n\n"
    await update.message.reply_text(reply_text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()