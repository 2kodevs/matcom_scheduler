from telegram.ext import Filters

private_text_filter = Filters.text & ~Filters.command & Filters.private
