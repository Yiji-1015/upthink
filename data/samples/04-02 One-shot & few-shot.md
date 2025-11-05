---
created: 2025-05-29
modified: 2025-05-29
image_processed: False
tags: 
  - prompt-engineering
  - google-whitepaper
  - one-shot
  - few-shot
url:
  - https://www.kaggle.com/whitepaper-prompt-engineering
desc: Prompt Engineering에서 One-shot과 Few-shot의 특징 (구글의 whitepaper)
---

>Examples are especially useful when you want to steer the model to a certain output structure or pattern.

Prompt에 예시(Example)를 포함하면, LLM이 output을 특정 구조(Structure)나 패턴(Pattern)에 맞추어 생성하도록 유도할 수 있다. 예시의 수에 따라 One-shot, Few shot으로 구분된다.

One-shot은 단일 예시(single example)를 제공하는 것으로, 모델이 이 예시를 모방(imitate)하여 주어진 task를 어떻게 완료할 지 알 수 있다.

반면, Few-shot은 여러 예시(multiple example)를 제공하는 것이다. 이는 모델에게 일관된 규칙(pattern)을 알려준다. 하나의 예시를 모방하는 것을 넘어, 여러 예시 속에서 공통된 pattern을 파악하고 따르도록 한다. 따라서 모델은 예시가 많을수록 의도한 pattern을 따를 가능성이 높아진다.

Few-shot에서 필요한 예시의 수는 task의 복잡성(complexity), 예시의 품질(quality), 사용 중인 모델의 성능에 따라 달라진다. 일반적으로 최소 3-5개의 예시를 사용하는데, 복잡성이 높은 task에는 이보다 더 많은 예시가 필요하거나, 모델의 입력 길이 제한(input length limitation)으로 더 적은 예시를 사용해야 할 수 있다.

예시의 내용을 작성할 땐 task와 관련된 것들로 구성해야 한다. 예시는 다양하고, 높은 품질로 잘 작성되어야 한다. 작은 것 하나가 모델을 혼란스럽게(confuse) 하여 원하는 결과를 얻지 못할 수 있다.
다양한 케이스의 입력에 대해 강건한(robust) 출력을 얻고자 하는 경우, 예시에 edge case를 포함하는 것이 좋다. Edge case는 특수한 상황에 대한 대처법을 알려주는 가이드라인이라고 할 수 있다.

![[04-02 One-shot & few-shot.png]]
![[04-02 One-shot & few-shot-1.png]]