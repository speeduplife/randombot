import asyncio
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
from vkwave.bots.utils.uploaders import PhotoUploader
from vkwave.bots.core.dispatching import filters
from random import randint
import re


bot = SimpleLongPollBot(tokens=[''],
                        group_id=)

def newWordWrite(mes) -> str:
    with open("words.txt", "a", encoding='utf-8') as wordsf:
        messagewrite = mes + "\n"
        wordsf.writelines(messagewrite)

def newPhotoWrite(photo) -> str:
    with open("photos.txt", "a", encoding='utf-8') as photosf:
        photowrite = photo + "\n"
        photosf.writelines(photowrite)

@bot.message_handler(bot.text_contains_filter(["сколько слов знаешь", "сколько знаешь слов", "сколько ты знаешь слов", "Сколько знаешь слов", "Сколько ты знаешь слов", "Сколько слов знаешь"]))
async def wordsCount(event: SimpleBotEvent) -> str:
        with open('words.txt', "r", encoding='utf-8') as f:
            words_array = str([row.strip() for row in f])
            words_array = words_array.split()
            count_words = len(words_array)
            count_words = str(count_words)
            await event.answer("Я знаю " + count_words + " слов")


@bot.message_handler(bot.event_type_filter("message_new"))
async def randomPhrase(event: SimpleBotEvent) -> str:
        message = event.text
        random_int = randint(1, 20)
        if event.object.object.message.attachments == []:
            print("RANDOM:", random_int)
            newword = False

            with open('words.txt', "r", encoding='utf-8') as file:
                for line in file:
                    if message in line:
                        newword = True

            if newword == False:
                message = event.text
                newWordWrite(message)
                print("NEW:", message)

            if random_int == 1:
                with open('words.txt', "r", encoding='utf-8') as f:
                    i = 1
                    answerphrase = ""
                    random = randint(1, 10)
                    print(random)
                    while i < random:
                        with open('words.txt', "r", encoding='utf-8') as f:
                            words_array_rig = str([row.strip() for row in f])
                            words_array = words_array_rig.split()
                            count_words_in_words_array = len(words_array)
                            random_word = randint(1, count_words_in_words_array)
                            answerphrase = answerphrase + " " + words_array[random_word]
                            answerphrase = re.sub(r'(id|1|2|3|4|5|6|7|8|9|0|,|\||\[|\]|\(|\)|\')', '', answerphrase)
                            i = i + 1
                    print("PHRASE:", answerphrase)           
                    await event.answer(answerphrase.casefold())


            if random_int == 5:
                with open("photos.txt", "r", encoding='utf-8') as photosf:
                    photos_array_rig = str([row.strip() for row in photosf])
                    photos_array = photos_array_rig.split()
                    count_photos_in_photos_array = len(photos_array)
                    global random_photo
                    randint_photo = randint(1, count_photos_in_photos_array)
                    print(randint_photo)
                    random_photo = photos_array[randint_photo]
                    random_photo = re.sub(r'(\[|\]|\'|,)', '', random_photo)
                    print(random_photo)


                with open('words.txt', "r", encoding='utf-8') as f:
                    random = randint(1, 20)
                    words_array_rig = str([row.strip() for row in f])
                    words_array = words_array_rig.split()
                    count_words_in_words_array = len(words_array)
                    random_word_1 = randint(1, count_words_in_words_array)
                    random_word_2 = randint(1, count_words_in_words_array)
                    random_word_3 = randint(1, count_words_in_words_array)
                    user = event.user_id
                    answerphrase = words_array[random_word_1] + " " + words_array[random_word_2] + " " + words_array[random_word_3]
                    answerphrase = re.sub(r'(id|1|2|3|4|5|6|7|8|9|0|,|\||\[|\]|\(|\)|\')', '', answerphrase)
                    photo = await PhotoUploader(bot.api_context).get_attachment_from_link(peer_id=user, link=random_photo)
                    print("PHRASE:", answerphrase)           
                    await event.answer(answerphrase.casefold(), attachment=photo)
        else:
            photo_url = event.object.object.message.attachments[0].photo.sizes[-1].url
            newPhotoWrite(photo_url)


bot.run_forever()
