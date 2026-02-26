import openai
import inspect

print('OpenAI class init signature:')
print(inspect.signature(openai.OpenAI))

# try to see default config values
print('\nOpenAI class doc:')
print(openai.OpenAI.__doc__[:1000])
