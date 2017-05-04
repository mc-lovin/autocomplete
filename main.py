import os
from subprocess import call

AUTOCOMPLETE_TEMPLATE = """
{}()
{{
    local cur opts
    cur="${{COMP_WORDS[COMP_CWORD]}}"
    opts="{}"
    COMPREPLY=( $(compgen -W "${{opts}}" -- ${{cur}}) )
}}
complete -F {} {}
"""

PATH_TO_COMPLETION_DIR = "/etc/bash_completion.d/"

PATH_TO_BASH_PROFILE = "~/.bash_profile"

PATH_TO_COMPLETION_SCRIPT = "/etc/bash_completion.d/_auto_complete"

def require_sudo(function):
	def wrapper(*args, **kwargs):
		call(["sudo", "ls"])
		return function(*args, **kwargs)

	return wrapper


class AutoComplete(object):
	def __init__(self):
		self.output = ""

	def add(self, command, options):
		print command, options
		self.output = self.output + AUTOCOMPLETE_TEMPLATE.format(
			'__' + command,
			' '.join(options),
			'__' + command,
			command
		)

	def read(self, input_file):
		for line in file(input_file):
			tokens = line.strip('\n').split(' ')
			command, options = tokens[0], filter(len, tokens[1:])
			self.add(command, options)

	def check_command_at_boot():
		path = os.expanduser(PATH_TO_BASH_PROFILE)
		if not os.path.isfile(path):
			return False
		content = ''.join()


	@require_sudo
	def write(self):
		if not os.path.isdir(PATH_TO_COMPLETION_DIR):
			call(["sudo", "mkdir", PATH_TO_COMPLETION_DIR])

		# HACK TO GIVE PERMISSION SO THAT WE CAN WRITE TO IT LATER
		call(["sudo", "touch", PATH_TO_COMPLETION_SCRIPT])
		call(["sudo", "chmod", "777", PATH_TO_COMPLETION_SCRIPT])

		with open(PATH_TO_COMPLETION_SCRIPT, 'w+') as handle:
			handle.write(self.output)


	def execute(self, input_file):
		self.read(input_file)
		self.write()

autocomplete = AutoComplete()
autocomplete.execute('dummy')
