
import typing


class CommandNode:

    def __init__(self, handler: typing.Union[None, callable]):
        self._cb = handler
        self._subcmds = {}

    def add_sub_command(self, command_str: str, command_node):
        self._subcmds[command_str] = command_node
        return self._subcmds[command_str]

    def autocomplete(self, cmd_list: list):
        curcmd = self
        # Walk the command tree
        for cmdstr in cmd_list[:-1]:
            if cmdstr in curcmd._subcmds:
                curcmd = curcmd._subcmds[cmdstr]
            else:
                # Cannot autocomplete
                return cmd_list

        count = 0
        match = ""
        for cmdstr in curcmd._subcmds:
            if cmdstr.startswith(cmd_list[-1]):
                count += 1
                match = cmdstr

        if count == 1 and match:
            return cmd_list[:-1] + [match]
        return cmd_list

    def call(self, command_list: list):
        curcmd = self
        arg_start_index = 0
        for index, cmdstr in enumerate(command_list):
            if cmdstr in curcmd._subcmds:
                curcmd = curcmd._subcmds[cmdstr]
            else:
                arg_start_index = index
        curcmd._cb(" ".join(command_list[arg_start_index:]))
