from src.exports.commands.config_cmd.query_fn import query_fn_cmd
from src.exports.commands.config_cmd.list_queryfn import list_query_fn_cmd
from src.exports.commands.config_cmd.list_theme import list_theme_cmd
from src.exports.commands.config_cmd.theme import theme_cmd
from src.exports.commands.config_cmd.view_array import view_array_cmd
from src.exports.commands.config_cmd.view_node_data import view_node_data_cmd
from src.exports.commands.config_cmd.view_node_info import view_node_info_cmd

exported_config_cmds = [
    query_fn_cmd,
    list_query_fn_cmd,
    list_theme_cmd,
    theme_cmd,
    view_array_cmd,
    view_node_data_cmd,
    view_node_info_cmd
]