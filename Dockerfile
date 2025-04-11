FROM python
WORKDIR /CHATBOT
COPY .  /CHATBOT
RUN pip install --upgrade pip
RUN /bin/sh -c "pip install -r requirements.txt"

ENV BASICURL = https://genai.hkbu.edu.hk/general/rest
ENV MODELNAME = gpt-4-o-mini
ENV APIVERSION = 2024-05-01-preview
ENV GPT_ACCESS_TOKEN "a5d67602-ced8-4b3f-926b-8e07012a59ba"
ENV TLG_ACCESS_TOKEN "7945850444:AAEuld73YYsKSi3Cn_1LCGOyWNMyiqz1l68"

CMD python chatbot.py