
import typing


class CommandNode:

    def __init__(self, handler: typing.Union[None, callable], *uargs, **ukwargs):
        self._cb = handler
        self._subcmds = {}
        self._uargs = uargs
        self._ukwargs = ukwargs

    def add_sub_command(self, command_str: str, sub_handler: typing.Union[None, callable], *uargs, **ukwargs):
        self._subcmds[command_str] = CommandNode(sub_handler, *uargs, **ukwargs)
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
        try:
            for cmdstr in curcmd._subcmds:
                if cmdstr.startswith(cmd_list[-1]):
                    count += 1
                    match = cmdstr
        except IndexError:
            return cmd_list
        if count == 1 and match:
            return cmd_list[:-1] + [match]
        return cmd_list

    def call(self, command_list: list):
        curcmd = self
        arg_start_index = 0
        for index, cmdstr in enumerate(command_list):
            if cmdstr in curcmd._subcmds:
                curcmd = curcmd._subcmds[cmdstr]
                arg_start_index = index+1
        curcmd._cb(" ".join(command_list[arg_start_index:]), *curcmd._uargs, **curcmd._ukwargs)
