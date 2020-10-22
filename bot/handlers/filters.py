from telegram.ext import CommandHandler, Filters

private_text_filter = Filters.text & ~Filters.command & Filters.private
