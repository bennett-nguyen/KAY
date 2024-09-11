from src.exports.commands.home import home_cmd
from src.exports.commands.insert import insert_cmd
from src.exports.commands.remove import remove_cmd
from src.exports.commands.extend import extend_cmd
from src.exports.commands.update import update_cmd
from src.exports.commands.query_fn import query_fn_cmd
from src.exports.commands.clear import clear_cmd
from src.exports.commands.query import query_cmd
from src.exports.commands.list_queryfn import list_query_fn_cmd
from src.exports.commands.list_theme import list_theme_cmd
from src.exports.commands.theme import theme_cmd

exported_core_cmds = [
    home_cmd,
    insert_cmd,
    remove_cmd,
    extend_cmd,
    update_cmd,
    query_fn_cmd,
    clear_cmd,
    query_cmd,
    list_query_fn_cmd,
    list_theme_cmd,
    theme_cmd
]
