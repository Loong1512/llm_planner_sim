from openai import OpenAI
client = OpenAI()

user1 = '''
import numpy as np
from env_utils import execute
from perception_utils import parse_query_obj
import action_utils import composer
objects = ['blue block', 'yellow block', 'mug']
place the blue block on the yellow block, and avoid the mug at all time.
composer("grasp the blue block while keeping at least 15cm away from the mug")
composer("back to default pose")
composer("move to 5cm on top of the yellow block while keeping at least 15cm away from the mug")
composer("open gripper")
# done
objects = ['airpods', 'drawer']
Open the drawer slowly.
composer("grasp the drawer handle, at 0.5x speed")
composer("move away from the drawer handle by 25cm, at 0.5x speed")
composer("open gripper, at 0.5x speed")
# done
objects = ['tissue box', 'tissue', 'bowl']
Can you pass me a tissue and place it next to the bowl?
composer("grasp the tissue")
composer("back to default pose")
composer("move to 10cm to the right of the bowl")
composer("open gripper")
composer("back to default pose")
# done
objects = ['charger', 'outlet']
unplug the charger from the wall.
composer("grasp the charger")
composer("back to default pose")
# done
objects = ['grape', 'lemon', 'drill', 'router', 'bread', 'tray']
put the sweeter fruit in the tray that contains the bread.
composer("grasp the grape")
composer("back to default pose")
composer("move to the top of the tray that contains the bread")
composer("open gripper")
# done
objects = ['marbles', 'tray', 'broom']
Can you sweep the marbles into the tray?
composer("grasp the broom")
composer("back to default pose")
composer("push the marbles into the tray")
# done
objects = ['orange', 'QR code', 'lemon', 'drawer']
put the sour fruit into the top drawer.
composer("grasp the top drawer handle")
composer("move away from the top drawer handle by 25cm")
composer("open gripper")
composer("back to default pose")
composer("grasp the lemon")
composer("move to 10cm on top of the top drawer")
composer("open gripper")
# done
objects = ['fridge', 'hot soup']
Open the fridge door and be careful around the hot soup.
composer("grasp the fridge handle and keep at least 15cm away from the hot soup")
composer("move away from the fridge handle by 25cm and keep at least 15cm away from the hot soup")
composer("open gripper")
# done
objects = ['cyan bowl', 'yellow bowl', 'box', 'ice cream']
move to the top of the cyan bowl.
composer("move to the top of the cyan bowl")
# done
objects = ['drawer', 'umbrella']
close the drawer.
composer("push close the drawer handle by 25cm")
# done
objects = ['iPhone', 'airpods']
slide the iPhone towards the airpods.
composer("push the iPhone towards the airpods")
# done
objects = ['plate', 'steak', 'fork', 'knife', 'spoon']
Could you please set up the fork for the steak for me?
composer("grasp the fork")
composer("back to default pose")
composer("move to 10cm to the right of the plate")
composer("open gripper")
composer("back to default pose")
# done
objects = ['lamp', 'switch']
Turn off the lamp.
composer("close the gripper")
composer("move to the center of the switch")
composer("back to default pose")
# done
objects = ['beer']
turn close the beer.
composer("grasp the beer cap")
composer("turn clockwise by 180 degrees")
composer("back to default pose")
# done
objects = ['steak', 'grill', 'plate']
Take the steak out of the grill and put it flat on the plate.
composer("grasp the steak")
composer("back to default pose")
composer("rotate the gripper to be 45 degrees slanted relative to the plate")
composer("move to 10cm on top of the plate")
composer("open gripper")
composer("back to default pose")
# done
'''
user2 = '''
objects = ['bin', 'rubbish', 'tomato1', 'tomato2']
# Query: chuck way any rubbish on the table rubbish.
'''

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  stop=['# Query:', 'objects = '],
  temperature=0,
  max_tokens=512,
  messages=[
    {"role": "system", "content": "You are a helpful assistant that pays attention to the user's instructions and writes good python code for operating a robot arm in a tabletop environment."},
    {"role": "user", "content": f"I would like you to help me write Python code to control a robot arm operating in a tabletop environment. Please complete the code every time when I give you new query. Pay attention to appeared patterns in the given context code. Be thorough and thoughtful in your code. Do not include any import statement. Do not repeat my question. Do not provide any text explanation (comment in code is okay). I will first give you the context of the code below:\n\n```\n{user1}\n```\n\nNote that x is back to front, y is left to right, and z is bottom to up."},
    # {"role": "user", "content": "我希望你能帮我补全代码，首先我会给你一些示例如下{user1}，通过示例学习规律，接下来我会给出一段上下文，请你续写后面的部分，严格仿照示例的风格和格式，只输出代码部分不输出任何文字说明（注释除外）。"},
    {"role": "assistant", "content": "Got it. I will complete what you give me next."},
    {"role": "user", "content": user2}
  ]
)

print(completion.choices[0].message.content)
