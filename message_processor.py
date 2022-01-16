
from spellchecker import SpellChecker

from kaspy.kaspa_clients import RPCClient

from .defines import commands as cmds, messages as msgs
from spellchecker import SpellChecker
import discord

spell_checker = SpellChecker()


class message_processor:

  def __init__(self, msg : discord.Message, client:discord.Client):
    self.kaspa_client = RPCClient()
    self.kaspa_client.auto_connect()
    self.client = client
    self.input_message = msg
    self.name = client.user
    self.commands = self._get_commands()
    self.partner = msg.user
    self.messages = list(msgs.INITAL_GREETING(self.partner, self.name))

    self.cmd_to_func = {
        cmds.DEVFUND : self.devfund,
        cmds.HELP : self.help,
        cmds.SUGGESTION : self.suggestion,
        cmds.BALANCE : self.balance,
        cmds.MINING_REWARDS : self.mining_rewards,
        cmds.MINING_RATE : self.mining_rate,
        cmds.STATS : self.stats
    }

  def answer(self):
    self.preprocess_message()
    self.process_message()
    self.messages.append(msgs.TIPS(self.name))
    return self.input_message.channel.send('\n\n'.join(self.messages))

  def preprocess_message(self):
    self.input_message.content = self.input_message.content[len(self.name)+1:]
    self.input_message.content = self.input_message.content.lower()

  def process_message(self):
    if self.commands:
      for command in self.commands:
        if command[0] in self.cmd_to_func.keys():
          self.cmd_to_func[command[0]]()
        else:
          self.invalid_command(command)
    elif not self.input_message.content:
      self.reference_only()
    else:
      self.no_commands()

  def _get_commands(self):
    for command in self.msg.content.split('$'):
        self.commands.append(command.split())

  def reference_only(self):
    self.output_msg + '\n\n Hello!'

  def no_commands(self):
    self.output_sg + f'\n\n I do not understand, perhaps I can help with `@{self.name} ${cmds.HELP}`'

  def invalid_command(self, command):
    likely_command_str = None
    for candidate in spell_checker.candidates(command):
      if candidate in self.message_to_func.keys():
        likely_command_str = f' - Perhaps you meant `${candidate}`'
        break
    if likely_command_str:
      self.messages.append(f'I do not understand the command: `${command}`', + f'{likely_command_str}')
    else:
      self.messages.append(f'I do not understand the command: `${command}` \n' + 
                           f'type `@{self.name} ${cmds.cmds}` for a list of available commands')
    
  def devfund(self):
    raise NotImplementedError
  
  def help(self):
    raise NotImplementedError
  
  def suggestion(self):
    raise NotImplementedError
  
  def balance(self):
    raise NotImplementedError
  
  def mining_rewards(self):
    raise NotImplementedError
  
  def mining_rate(self):
    raise NotImplementedError
  
  def stats(self):
    raise NotImplementedError
  
  def _retrive_balance(self, addr):
    resp = self.kaspa_client.request('getBalanceByAddressRequest', {'addr' : addr})
    return resp['balance']
  
  def _get_hashrate(self):
    raise NotImplementedError