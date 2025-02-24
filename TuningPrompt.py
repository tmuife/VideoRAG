PROMPTS = {}
PROMPTS[
    "videorag_response"
] = """---Role---

You are a helpful assistant responding to a query with retrieved knowledge.

---Goal---

Generate a response of the target length and format that responds to the user's question with relevant general knowledge.
Summarize useful and relevant information from the retrieved text chunks and the information retrieved from videos, suitable for the specified response length and format.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Retrieved Information From Videos---

{video_data}

---Retrieved Text Chunks---

{chunk_data}

---Goal---

Generate a response of the target length and format that responds to the user's question with relevant general knowledge.
Summarize useful and relevant information from the retrieved text chunks and the information retrieved from videos, suitable for the specified response length and format.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.
Reference relevant video segments within the answers, specifying the video name and start & end timestamps. Use the following reference format:

---Example of Reference---

In one segment, the film highlights the devastating effects of deforestation on wildlife habitats [1]. Another part illustrates successful conservation efforts that have helped endangered species recover [2].

#### Reference:
[1] video_name_1, 05:30, 08:00  
[2] video_name_2, 25:00, 28:00 

---Notice---
Please add sections and commentary as appropriate for the length and format if necessary. Format the response in Markdown.
"""


sys_prompt_fall = """---Role---

You are a helpful assistant responding to a query with retrieved knowledge.

---Goal---

Generate a response of the target length and format that responds to the user's question with relevant general knowledge.
Summarize useful and relevant information from the retrieved text chunks and the information retrieved from videos, suitable for the specified response length and format.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

Multiple Paragraphs

---Retrieved Information From Videos---


-----Retrieved Knowledge From Videos-----
```csv
"video_name",   "start_time",   "end_time",     "content"
"Elderly-Fall", "0:0:0",        "0:0:10",       "Caption:
The video shows a sequence of events captured by a security camera in an outdoor area adjacent to a building with white brick walls and blue trim. The timestamp indicates the footage was recorded on October 17, 2021, at around 10:34 AM.Initially, a person dressed in dark clothing is seen bending over near some scattered items on the ground, possibly picking something up or examining it closely. As time progresses, this individual appears to lose balance and falls onto their back amidst various objects such as shoes and other miscellaneous items spread out nearby.Subsequently, text overlays appear intermittently throughout the frames. At one point, large Chinese characters "刘乐页" (Liu Le Ye) are displayed prominently across the screen, followed by another overlay showing the date "10月17日" (October 17). Later, additional text appears stating "孙女在监控中" (Sun Nv is under surveillance), suggesting that someone named Sun Nv might be being monitored through this footage.Throughout these moments, the environment remains consistent with no significant changes except for the movements and actions of the individual who eventually lies motionless among the scattered belongings after falling down.
Transcript:
[0.00s -> 10.00s]  Thank you."
```


---Retrieved Text Chunks---

Caption:
Here is a detailed description of the video:1. **Actions in Chronological Order**:   - At 10:34:16, a person wearing dark clothing walks towards an area with various items.   - By 10:34:20, this individual has fallen to the ground near some scattered objects.2. **Identification of Individuals and Roles**:   - The only visible individual throughout the sequence appears to be one person who falls after walking.3. **Specific Events**:   - Fall: Around 10:34:20, there's a noticeable fall by the individual on the concrete surface next to the building entrance.4. **Classification of Behaviors**:   - Walking (10:34:16)   - Falling (10:34:20)5. **Tracking Object Movement**:   - No specific object movement trajectory is described within these frames; however, it can be noted that personal belongings are scattered around during the incident.6. **Analysis of Group Behavior**:   - There is no group behavior observed or changes mentioned as the scene focuses solely on a single individual’s actions.7. **Identification and Tracking Specific Objects**:   - A bag-like item is seen lying close to where the individual fell but remains stationary through the duration captured.Overall, the footage captures a momentary event involving an individual falling while carrying out what seems like routine activity outside a building.
Transcript:
[0.00s -> 10.00s]  Thank you.

---Goal---

Generate a response of the target length and format that responds to the user's question with relevant general knowledge.
请按照以下格式生成视频描述：

视频描述
视频展示了一个{环境描述}，{场景特点}。{人物活动描述}。

对象特征
年龄段：{年龄描述，例如：成年人、青少年等}
穿着：{服饰描述，例如：外套、卫衣、长裤等}
携带物品：{携带物品，例如：水杯、手机、背包等}
行为序列
• {时间段1}：{人物行为1}  
• {时间段2}：{人物行为2}  
• {时间段3}：{人物行为3}  
请按照时间顺序，清晰描述视频中的关键行为。

输出规范
1. 基础判断
◦ 异常停留: {0-1之间的数值}  
◦ 入侵检测: {0-1之间的数值}  
◦ 人员跌倒: {0-1之间的数值}  
◦ 包裹投递: {0-1之间的数值}  
请为每项指标提供 0~1 之间的数值，表示该事件的可能性。

2. 事件分类
◦ {事件类型，例如：异常停留、人员聚集等}  
3. 行为性质
◦ {行为性质，例如：可疑行为、正常行为等}  


---Notice---
Please add sections and commentary as appropriate for the length and format if necessary. Format the response in Markdown.

"""

sys_prompt_multi_object = """---Role---

You are a helpful assistant responding to a query with retrieved knowledge.

---Goal---

Generate a response of the target length and format that responds to the user's question with relevant general knowledge.
Summarize useful and relevant information from the retrieved text chunks and the information retrieved from videos, suitable for the specified response length and format.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

Multiple Paragraphs

---Retrieved Information From Videos---


-----Retrieved Knowledge From Videos-----
```csv
"video_name",   "start_time",   "end_time",     "content"
"Multi-Ojbect", "0:0:0",        "0:0:30",       "Caption:
The video takes place in a modern, well-lit hallway with reflective surfaces and elevator doors. The walls are decorated with red Chinese New Year decorations featuring the character "福" (fu), which means good fortune or happiness.Initially, two individuals stand near an elevator door on the left side of the frame. One person is wearing a gray hoodie and black pants, while the other is dressed in a black vest over a red shirt and dark pants. They appear to be engaged in conversation as they move slightly within the frame. A third individual, who was previously visible through the glass wall behind them, now stands closer to the camera but remains partially obscured by it.As the scene progresses, another individual enters from the right side of the frame, wearing a pink sweatshirt with large letters "E3P" on it. This new person interacts briefly with the first two before walking away towards the center of the frame.The three individuals continue their interaction, moving around the space. At one point, the person in the gray hoodie walks past the others, heading towards the right side of the frame. Meanwhile, the person in the black vest stays relatively stationary near the elevator doors.Throughout the video, there are no significant changes in the environment or lighting, maintaining a consistent setting focused on the interactions between the individuals in this modern hallway adorned for the Chinese New Year celebration.
Transcript:
[0.00s -> 2.00s]  You know?
[2.00s -> 3.00s]  Oh.
[3.00s -> 5.00s]  See?
[5.00s -> 6.00s]  Smash.
[6.00s -> 9.00s]  Oh, you're going to get my shoulder.
[9.00s -> 12.00s]  I'm going to go.
[12.00s -> 14.00s]  I'm going to go.
[14.00s -> 15.00s]  I'm going to go.
[15.00s -> 18.00s]  Oh.
[18.00s -> 19.00s]  Oh.
[19.00s -> 20.00s]  You're really?
[20.00s -> 21.00s]  Yeah.
[21.00s -> 23.00s]  Okay.
[23.00s -> 25.00s]  I don't know."
```


---Retrieved Text Chunks---

Caption:
Here is a detailed description of the video based on your instructions:1. **List all actions in chronological order**:   - [0.00s -> 2.00s]: Two individuals are standing and conversing.   - [2.00s -> 3.00s]: One individual turns to face another person entering from behind.   - [3.00s -> 5.00s]: The two original individuals continue their conversation, with one gesturing towards something off-screen.   - [5.00s -> 6.00s]: A third individual wearing a pink hoodie enters the frame from the left side.   - [6.00s -> 9.00s]: The interaction between the three appears more animated; they seem engaged in a discussion or confrontation.   - [9.00s -> 12.00s]: There seems to be an escalation as if preparing for some physical action.   - [12.00s -> 14.00s]: All three individuals move closer together, possibly indicating tension or preparation for conflict.   - [14.00s -> 15.00s]: They appear ready to act but do not engage physically yet.   - [15.00s -> 18.00s]: The group's attention shifts slightly away from each other toward something else out of view.   - [18.00s -> 19.00s]: Slight movement suggests anticipation or readiness for further action.   - [19.00s -> 20.00s]: The first speaker asks a question, indicated by "You're really?" followed by acknowledgment "Yeah."   - [20.00s -> 21.00s]: Confirmation response "Okay" implies agreement or understanding.   - [21.00s -> 23.00s]: The phrase "I don't know." indicates uncertainty or doubt.2. **Identify individuals and their roles**:   - Person A: Wearing a black vest over a red shirt with 'PATIENCE' written on it.   - Person B: Wearing a gray jacket and dark pants.   - Person C: Enters later wearing a bright pink hoodie with text on it.3. **Detect specific events**:   - No significant fights, falls, broken objects, etc., occur throughout this sequence.4. **Classify behaviors**:   - Conversations (mainly among the initial two).   - Introduction of new individual.   - Increased engagement suggesting possible escalation into a potential confrontation.5. **Track object movement**:    - Individuals enter/exit through glass doors marked with Chinese characters and decorations.6. **Analyze group behavior patterns**:   - Initial calm conversations shift to heightened alertness and slight movements suggestive of impending action.   - Group dynamics show increased focus and collective anticipation before any actual physical altercation occurs.7. **Identify and track specific objects**:   - Glass doors remain static except when used by individuals moving in/out.This structured analysis provides a comprehensive overview of the interactions and environment captured in the provided frames.
Transcript:
[0.00s -> 2.00s]  You know?
[2.00s -> 3.00s]  Oh.
[3.00s -> 5.00s]  See?
[5.00s -> 6.00s]  Smash.
[6.00s -> 9.00s]  Oh, you're going to get my shoulder.
[9.00s -> 12.00s]  I'm going to go.
[12.00s -> 14.00s]  I'm going to go.
[14.00s -> 15.00s]  I'm going to go.
[15.00s -> 18.00s]  Oh.
[18.00s -> 19.00s]  Oh.
[19.00s -> 20.00s]  You're really?
[20.00s -> 21.00s]  Yeah.
[21.00s -> 23.00s]  Okay.
[23.00s -> 25.00s]  I don't know.


Caption:
1. **Actions in Chronological Order**:   - The person is standing still, looking around.2. **Identification of Individuals and Roles**:   - There is one individual present throughout the video.   - No other individuals are visible or mentioned.3. **Specific Events**:   - No notable events such as fights, falls, or broken objects occur during this time period.4. **Classification of Behaviors**:   - The primary behavior observed is a static stance with minimal movement from the person.5. **Tracking Object Movement**:   - No specific object movements are tracked within this description; only the actions of the person are described.6. **Analysis of Group Behavior**:   - Only one individual's behavior is analyzed. They remain stationary most of the time with slight changes in posture but no significant group activity occurs.7. **Identification and Tracking Specific Objects**:   - No specific objects are identified for tracking movement paths.In summary, the video depicts an individual who stands mostly motionless while occasionally shifting their gaze slightly to different directions inside what appears to be a modern building lobby adorned with festive decorations.
Transcript:
[0.00s -> 7.00s]  The

---Goal---

Generate a response of the target length and format that responds to the user's question with relevant general knowledge.
请按照以下格式生成视频描述：

视频描述
视频展示了一个{环境描述}，{场景特点}。{人物活动描述}。

对象特征
年龄段：{年龄描述，例如：成年人、青少年等}
穿着：{服饰描述，例如：外套、卫衣、长裤等}
携带物品：{携带物品，例如：水杯、手机、背包等}
行为序列
• {时间段1}：{人物行为1}  
• {时间段2}：{人物行为2}  
• {时间段3}：{人物行为3}  
请按照时间顺序，清晰描述视频中的关键行为。

输出规范
1. 基础判断
◦ 异常停留: {0-1之间的数值}  
◦ 入侵检测: {0-1之间的数值}  
◦ 人员跌倒: {0-1之间的数值}  
◦ 包裹投递: {0-1之间的数值}  
请为每项指标提供 0~1 之间的数值，表示该事件的可能性。

2. 事件分类
◦ {事件类型，例如：异常停留、人员聚集等}  
3. 行为性质
◦ {行为性质，例如：可疑行为、正常行为等}  

---Notice---
Please add sections and commentary as appropriate for the length and format if necessary. Format the response in Markdown.
"""

sys_prompt_long_stay = """---Role---

You are a helpful assistant responding to a query with retrieved knowledge.

---Goal---

Generate a response of the target length and format that responds to the user's question with relevant general knowledge.
Summarize useful and relevant information from the retrieved text chunks and the information retrieved from videos, suitable for the specified response length and format.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

Multiple Paragraphs

---Retrieved Information From Videos---


-----Retrieved Knowledge From Videos-----
```csv
"video_name",   "start_time",   "end_time",     "content"
"LongStay",     "0:0:0",        "0:0:30",       "Caption:
The video begins with a view of a concrete surface, possibly part of a rooftop or terrace area. The ground is cracked and worn out, surrounded by greenery on the left side. A person wearing white shoes appears in the frame from behind, walking along the edge near a brick wall that borders the area.As the scene develops, more details become visible: the person starts to walk away from the camera towards an open space below, which includes some buildings and vegetation. To the right, there are various items such as bamboo poles and other materials scattered around, indicating a construction site or storage area. The person continues walking down this path, passing by these items.The narrative progresses with the same individual now standing still on the pathway, facing slightly upwards, perhaps looking at something above them. The background remains consistent with dense foliage and several structures partially obscured by trees. The blue disc-like object seen earlier lies further down the path. Text appears in Chinese characters on the screen: '小晓筱' (Xiao Xiao Xiao) and '我说人间冷暖' (I say the coldness and warmth of human nature), suggesting a reflective or philosophical theme related to the content being shown.The video wraps up with the person turning their body slightly while remaining in place, continuing to look into the distance. The surroundings remain unchanged, maintaining focus on the pathway, the scattered materials, and the natural environment surrounding it.
Transcript:"
"LongStay",     "0:0:30",       "0:0:48",       "Caption:
The video begins with a view of an outdoor area filled with various items, including wooden poles and other materials stacked against the wall. A person wearing a white shirt and black shorts is seen crouching near some equipment under a makeshift shelter made of bamboo poles and tarpaulin. The background features lush greenery and a dirt path leading to another part of the area. The person stands up, walks towards the camera holding something in their hand, then turns around and starts walking down the dirt path.The scene continues with the same individual now further away from the camera, still on the dirt path surrounded by dense foliage and scattered red bricks. They are barefoot as they walk past more stacks of wood and other construction materials. As they move along the path, which curves slightly upwards, the surrounding environment remains consistent with previous frames, featuring bamboo structures and additional piles of materials like tires and tarps.
Transcript:
[0.00s -> 1.00s]  of the
[1.00s -> 2.00s]  question.
[2.00s -> 3.00s]  I have to say,
[3.00s -> 4.00s]  however,
[4.00s -> 5.00s]  actually,
[5.00s -> 6.00s]  he's
[6.00s -> 7.00s]  this time
[7.00s -> 8.00s]  she found
[8.00s -> 9.00s]  she's
[9.00s -> 10.00s]  she's
[10.00s -> 11.00s]  he's,
[11.00s -> 12.00s]  he's
[12.00s -> 13.00s]  many,
[13.00s -> 14.00s]  many times,
[14.00s -> 15.00s]  the
[15.00s -> 16.00s]  sure is,
[16.00s -> 17.00s]  the
[17.00s -> 18.00s]  the way,
[18.00s -> 19.00s]  the"
```


---Retrieved Text Chunks---

Caption:
1. **List all actions in chronological order**:   - The person is standing on a concrete surface near a brick wall.   - They throw an object, possibly a frisbee or disc, onto the ground below them.2. **Identify individuals and their roles**:   - One individual wearing white shoes, black shorts, and a light-colored shirt (possibly with text) appears to be throwing the object.3. **Detect specific events**:   - There are no significant fights, falls, broken cars, or other notable incidents detected during this sequence of frames.4. **Classify behaviors**:   - Walking: Person moves towards the edge where they threw the object.   - Throwing objects: Person throws something onto the ground from above.5. **Track object movement**:   - An object (possibly a frisbee or disc) is thrown by the person down into what seems like a lower area or yard.6. **Analyze group behavior**:   - No groups form; only one individual interacts throughout these sequences.7. **Identify and track specific objects**:   - Object trajectory: The frisbee-like item is seen falling downwards after being thrown by the person.Overall summary:In the video, there's a scene showing someone at the top of a structure who throws an object downward. This action takes place against a backdrop featuring greenery, buildings, and construction materials scattered around. Throughout the clip, the main focus remains on the act of throwing and observing the path of the object as it descends out of view.
Transcript:


Caption:
The video begins with a scene showing an outdoor area filled with various items, including wooden poles and other construction materials. A person wearing a white shirt and black shorts is seen sitting near the center of this cluttered space under a makeshift shelter supported by bamboo poles. The background features lush greenery and some buildings in the distance.As the sequence progresses, the same individual starts walking along a dirt path that runs alongside the cluttered area. This path appears to be elevated, as there are more trees and vegetation visible on one side. The person continues to walk down the path away from the camera's perspective, maintaining their position throughout the frames.Throughout the entire clip, no significant changes occur except for the movement of the individual who walks further into the distance. There are no specific events such as fights or falls, nor any notable movements of objects apart from the person’s progression down the path. The environment remains consistent, featuring the same construction materials, bamboo supports, and natural surroundings without any new elements introduced during the sequence.
Transcript:
[0.00s -> 1.00s]  of the
[1.00s -> 2.00s]  question.
[2.00s -> 3.00s]  I have to say,
[3.00s -> 4.00s]  however,
[4.00s -> 5.00s]  actually,
[5.00s -> 6.00s]  he's
[6.00s -> 7.00s]  this time
[7.00s -> 8.00s]  she found
[8.00s -> 9.00s]  she's
[9.00s -> 10.00s]  she's
[10.00s -> 11.00s]  he's,
[11.00s -> 12.00s]  he's
[12.00s -> 13.00s]  many,
[13.00s -> 14.00s]  many times,
[14.00s -> 15.00s]  the
[15.00s -> 16.00s]  sure is,
[16.00s -> 17.00s]  the
[17.00s -> 18.00s]  the way,
[18.00s -> 19.00s]  the

---Goal---

Generate a response of the target length and format that responds to the user's question with relevant general knowledge.
请按照以下格式生成视频描述：

视频描述
视频展示了一个{环境描述}，{场景特点}。{人物活动描述}。

对象特征
年龄段：{年龄描述，例如：成年人、青少年等}
穿着：{服饰描述，例如：外套、卫衣、长裤等}
携带物品：{携带物品，例如：水杯、手机、背包等}
行为序列
• {时间段1}：{人物行为1}  
• {时间段2}：{人物行为2}  
• {时间段3}：{人物行为3}  
请按照时间顺序，清晰描述视频中的关键行为。

输出规范
1. 基础判断
◦ 异常停留: {0-1之间的数值}  
◦ 入侵检测: {0-1之间的数值}  
◦ 人员跌倒: {0-1之间的数值}  
◦ 包裹投递: {0-1之间的数值}  
请为每项指标提供 0~1 之间的数值，表示该事件的可能性。

2. 事件分类
◦ {事件类型，例如：异常停留、人员聚集等}  
3. 行为性质
◦ {行为性质，例如：可疑行为、正常行为等}  

---Notice---
Please add sections and commentary as appropriate for the length and format if necessary. Format the response in Markdown.
"""
from openai import OpenAI, AsyncAzureOpenAI, APIConnectionError, RateLimitError
from decouple import config
query = "Please list all actions in the video along with their timestamps and descriptions."
client = OpenAI(api_key=config("API_KEY"),base_url=config("BASE_URL"))
messages = []
messages.append({"role": "system", "content": sys_prompt_long_stay})
messages.append({"role": "user", "content": query})
response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages
    )
print(response.choices[0].message.content)