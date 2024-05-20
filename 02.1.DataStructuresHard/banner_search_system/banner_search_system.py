from collections import defaultdict
from heapq import heapify
from typing import List
import heapq


def normalize(
        text: str
) -> str:
    """
    Removes punctuation and digits and convert to lower case
    :param text: text to normalize
    :return: normalized query
    """

    return ''.join([char for char in text if (char.isalpha() or char.isspace())]).lower()


def get_words(
        query: str
) -> list[str]:
    """
    Split by words and leave only words with letters greater than 3
    :param query: query to split
    :return: filtered and split query by words
    """
    return list([word for word in query.split(' ') if len(word) > 3])


def build_index(
        banners: list[str]
) -> dict[str, list[int]]:
    """
    Create index from words to banners ids with preserving order and without repetitions
    :param banners: list of banners for indexation
    :return: mapping from word to banners ids
    """
    banners_index: dict = defaultdict(list[int])
    banners_words = [list(get_words(normalize(banner))) for banner in banners]
    for banner_id, banner in enumerate(banners_words):
        for word in banner:
            banners_index[word].append(banner_id)
    for banner in banners_index:
        banners_index[banner] = list(dict.fromkeys(banners_index[banner]))
    return dict(banners_index)


def get_banner_indices_by_query(
        query: str,
        index: dict[str, list[int]]
) -> list[int]:
    """
    Extract banners indices from index, if all words from query contains in indexed banner
    :param query: query to find banners
    :param index: index to search banners
    :return: list of indices of suitable banners
    """
    words: list[str] = list(set(get_words(normalize(query))))
    if not words:
        return []

    lst_out: list[int] = []
    word_banners: list[tuple[int, str]] = [(index[word][0], word) for word in words if word in index and len(index[word]) > 0]
    heapify(word_banners)
    how_many_words_took: dict[str: int] = {word: 0 for word in words}

    flag: bool = len(word_banners) == len(words)

    while flag:
        val = word_banners[0][0]
        streak_cnt = 0
        while word_banners and word_banners[0][0] == val:
            streak_cnt += 1
            word = heapq.heappop(word_banners)[1]
            how_many_words_took[word] += 1
            if how_many_words_took[word] == len(index[word]):
                flag = False
            else:
                heapq.heappush(word_banners, (index[word][how_many_words_took[word]], word))
        if streak_cnt == len(words):
            lst_out.append(val)
    return lst_out


#########################
# Don't change this code
#########################

def get_banners(
        query: str,
        index: dict[str, list[int]],
        banners: list[str]
) -> list[str]:
    """
    Extract banners matched to queries
    :param query: query to match
    :param index: word-banner_ids index
    :param banners: list of banners
    :return: list of matched banners
    """
    indices = get_banner_indices_by_query(query, index)
    return [banners[i] for i in indices]


#########################

BANNERS = [
    "Стиральный машина - Более 1000 модель!",
    "Маленькая стиральный машина - Машина недорого!",
    "Стиральная машина более 545 модель / holodilnik.ru",
    "Стиральная машина ведущий бренд - Неделя скидка!",
    "Стиральная машина - Кэшбэк до 20%",
    "Ремонт стиральная машина Выезд - 0 ₽. - Диагностика - 0 ₽.",
    "Ремонт стиральная машина - Скидка -20%",
    "Починка Стиральная Машина - Быстро и Недорого!",
    "Отремонтировать стиральная машина - на дом от 500₽!",
    "Холодильник.Ру - интернет магазин / holodilnik.ru",
    "Холодильник в Москва! - С гарантия 5 лет!",
    "Холодильник на goods.ru - Кэшбэк до 20%",
    "Купить холодильник на OZON.ru - Доставить завтра",
    "Десяток бренд холодильник - Неделя скидка!",
    "Ремонт холодильник! На дом - в Москва, вызов на дом!",
    "Ремонт холодильник? - Приехать прямо сейчас!",
    "Ремонт холодильник - Ремонт холодильник. Гарантия!",
    "Ремонт холодильник - В Москва и МО",
    "Скидка на джинсы - Покупать на Wildberries!",
    "Джинсы Levis / ozon.ru",
    "Стильный джинсы со скидка - Скидка 15% от 2999 р",
    "Джинсы от 600 руб. на Беру - Скидка и акция каждый день"
]


print(build_index(BANNERS))