import typing as tp


def median_from_list(nums: tp.Sequence[int]) -> float:
    if len(nums) % 2 == 1:
        return 1.0 * nums[len(nums) // 2]
    else:
        return (nums[len(nums) // 2] + nums[len(nums) // 2 - 1]) / 2


def find_median(nums1: tp.Sequence[int], nums2: tp.Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """

    #suggestion: while changing beg and end, I swear to cut equally from both sides.
    #Meaning that I will still have to search for median, including oddness.
    beg1: int = 0
    beg2: int = 0

    end1: int = len(nums1) - 1
    end2: int = len(nums2) - 1
    if k := (end1 - end2) > 2:
        cut: int = (k - 1) // 2
        beg1 += cut
        end1 -= cut
    elif k := (end2 - end1) > 2:
        cut: int = (k - 1) // 2
        beg2 += cut
        end2 -= cut
    #now we have almost equal sequences
    m1: int
    m2: int
    #until I reach the core of one(meaning actually almost of both) sequences, cutting off by half both
    while end1 - beg1 > 1 and end2 - beg2 > 1:
        m1 = (beg1 + end1) // 2  #mid or one bit lefter
        m2 = (beg2 + end2 + 1) // 2  #mid or one bit righter
        if nums1[m1] < nums2[m2]:
            #i wish i could do following:
            #beg1 = m1 - 1
            #end2 = m2 + 1
            #but instead i will cut equally
            cut = min(m1 - 1 - beg1, end2 - m2 - 1)
            beg1 += cut
            end2 -= cut
        else:
            # i wish i could do following:
            #beg2 = m2 - 1
            #end1 = m1 + 1
            # but instead i will cut equally
            cut = 1 + min(m2 - 1 - beg2, end1 - m1 - 1)
            beg2 += cut
            end1 -= cut
    #Each time we cut off on of halfs till the core. (core for odd len is mid cell and for even is two mid cells)
    #So for this: ---~~---, --~-- we will end up with smth like that: ---~~, ~--.
    #Now we guaranteed that cycle will eventually end since len will shorten until it is <= 2, for which value is <= 1
    lil_lst: list[int] = []
    if len(nums1) != 0:
        for i in range(beg1, end1 + 1):
            lil_lst.append(nums1[i])
    if len(nums2) != 0:
        for i in range(beg2, end2 + 1):
            lil_lst.append(nums2[i])
    lil_lst = sorted(lil_lst)
    return lil_lst[(len(lil_lst) - 1) // 2] / 2 + lil_lst[(len(lil_lst) - 1) // 2] / 2

#print(find_median([-5, 1, 2, 5, 9], [-2, -1, 0, 4]))
