from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = "8847412777:AAFIltf8GIaOlexDXjLbXLu9haWNf_Zq8EA"

tracked_movies = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Movie Ticket Alert Bot Started!\n\n"
        "Commands:\n"
        "/add movie city theater\n"
        "/list\n"
        "/remove movie"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args

        movie = args[0]
        city = args[1]
        theater = " ".join(args[2:])

        tracked_movies.append({
            "movie": movie,
            "city": city,
            "theater": theater
        })

        await update.message.reply_text(
            f"✅ Tracking added:\n"
            f"Movie: {movie}\n"
            f"City: {city}\n"
            f"Theater: {theater}"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/add movie city theater"
        )


async def list_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tracked_movies:
        await update.message.reply_text("No tracked movies.")
        return

    msg = "🎥 Tracking List:\n\n"

    for item in tracked_movies:
        msg += (
            f"Movie: {item['movie']}\n"
            f"City: {item['city']}\n"
            f"Theater: {item['theater']}\n\n"
        )

    await update.message.reply_text(msg)


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        movie_name = context.args[0]

        global tracked_movies
        tracked_movies = [
            x for x in tracked_movies
            if x["movie"].lower() != movie_name.lower()
        ]

        await update.message.reply_text(
            f"❌ Removed tracking for {movie_name}"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/remove movie"
        )


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_movies))
app.add_handler(CommandHandler("remove", remove))

print("Bot running...")
app.run_polling()