from defines import answers as ans
def adjoin_messages(*msgs):
  nl = '\n\n'
  return f"```{nl.join(msgs)}```"

def post_process_messages(*msgs):
  return adjoin_messages(ans.PREFACE, *msgs, ans.APPENDIX)