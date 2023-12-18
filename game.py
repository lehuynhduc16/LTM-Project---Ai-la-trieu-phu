import millionairedb
import random
import time
import sys

def main():
    def lets_wait(phrase, t):
        """ Thực hiện tạm dừng bằng dấu chấm """
        print(("\n\n %s" % phrase))
        sys.stdout.flush()
        for i in range(t):
            print(".")
            time.sleep(1)
            sys.stdout.flush()

    def intro_question(lvl):
        """ Giới thiệu câu hỏi"""
        lvl += 1
        bal = balance[lvl]
        v = [0 for i in range(9)]
        v[0] = "Đây là câu hỏi #%s trị giá $%s." % (lvl, bal)
        v[1] = "Chúng tôi sẽ đặt câu hỏi #%s để bạn giành được $%s." % (lvl, bal)
        v[2] = "Câu hỏi #%s cho $%s ngay bây giờ." % (lvl, bal)
        v[3] = "Đây là lượt câu hỏi #%s bạn sẽ nhận được $%s." % (lvl, bal)
        v[4] = "Bây giờ đến lượt câu hỏi #%s. Thắng $%s!" % (lvl, bal)
        v[5] = "Muốn $%s? Hãy xem bạn có thể trả lời câu hỏi #%s như thế nào!" % (bal, lvl)
        v[6] = "Hãy xem bạn mất bao nhiêu thời gian để trả lời câu hỏi #%s và giành được $%s!" % (lvl, bal)
        v[7] = "Bây giờ sang câu hỏi #%s. Nó có giá trị $%s." % (lvl, bal)
        v[8] = "Bạn muốn giành $%s? Đây là câu hỏi #%s." % (bal, lvl)
        n = int(random.random() * 9)
        return v[n]

    def ask_question(lvl):
        """ Generates số và câu hỏi từ database """
        to_return = "\n " + intro_question(lvl) + "\n "
        to_return += "=" * (len(to_return) - 3) + "\n "
        qnum = int(random.random() * 10)
        
        global q
        q = millionairedb.get_question(lvl, qnum)
        to_return += q[0]
        to_return += "\n A. " + q[1] + "\t\t B. " + q[2]
        to_return += "\n C. " + q[3] + "\t\t D. " + q[4]

        global correct_answer
        correct_answer = q[5]
        return to_return

    def check_answer(lvl):
        """ Check đáp án """
        answer = input("\n Bạn: ")
        answer = answer.lower()
        global correct_answer, q, help_friend_avail, help_50_avail, help_audience_avail

        if not (answer in acceptable_answers):  # Checking if the input makes sense
            print("""\n Tôi không hiểu ý của bạn.Nhập thư trả lời, 'help' để xem sự trợ giúp
                hoặc 'finish' để thoát khỏi trò chơi.""")
            check_answer(lvl)
        
        elif (answer == "help"):  # If 'help' was entered
            print("")
            if (help_50_avail): print(" " * 5 + help_50)
            if (help_friend_avail): print(" " * 5 + help_friend)
            if (help_audience_avail): print(" " * 5 + help_audience)
            if not (help_50_avail or help_friend_avail or help_audience_avail):  # If all lifelines were used
                print("\n" + " " * 5 + "Bạn đã dùng hết sự trợ giúp" )
            check_answer(lvl)

        elif (answer == "friend"):
            if (help_friend_avail == True):
                help_friend_avail = False
                if (random.random() < 0.7):  # There is a ~70% chance that friend's guess will be the right one
                    lets_wait("Gọi điện thoại cho người thân", 4)
                    print("\n Bạn của bạn nghĩ đáp án là %s." % correct_answer)
                    check_answer(lvl)
                else:  # In case two answers were eliminated by 50:50
                    while True:
                        i = int(random.random() * 4 + 1)
                        if (q[i] != "" and q[i] != correct_answer):
                            time.sleep("Calling your friend", 4)
                            print("\n Your friend thinks the correct answer is %s." % correct_answer)
                            check_answer(lvl)
            else:
                print("\n You already used this lifeline. Enter 'help' to see what other lifelines are left.")
                check_answer(lvl)

        elif (answer == "50"):
            if (help_50_avail == True):
                help_50_avail = False
                w = 0  # To track how many answers have been removed
                while True:
                    if w == 2:
                        break
                    i = int(random.random() * 4 + 1)
                    if (correct_answer != q[i] and q[i] != ""):
                        w += 1
                        q[i] = ""

                print("\n We eliminated two incorrect answers. The two remaining are:")
                temp = [" A. ", " B. ", " C. ", " D. "]
                for i in range(1, 5):
                    if (q[i] != ""):
                        print((temp[i-1] + q[i] + "\t\t"),)
                print("")
                check_answer(lvl)
        
            else:
                print("\n You already used this lifeline. Enter 'help' to see what other lifelines are left.")
                check_answer(lvl)

        elif (answer == "audience"):
            if (help_audience_avail == True):
                help_audience_avail = False
                while True:  # Just to
                    w = random.random()
                    if (w > 0.45):  # Just a number for the "majority" of the audience
                        w = int(w * 100)
                        break

                if (random.random() < 0.8):
                    audience_answer = correct_answer
                else:  # In case some answers were eliminated by 50:50
                    while True:
                        i = int(random.random() * 4 + 1)
                        if (q[i] != ""):
                            audience_answer = q[i]
                            break

                lets_wait("The audience is voting", 4)
                print("\n The majority (%s%%) of the audience think that the correct answer is %s." % (w, audience_answer))
                check_answer(lvl)
        
            else:
                print("\n You already used this lifeline. Enter 'help' to see what other lifelines are left.")
                check_answer(lvl)

        elif (answer == "finish"):
            print("\n You chose to finish the game, %s. You won $%s. Congratulations!" % (player, balance[lvl]))
            quit()

        elif (answer == "a" or answer == "b" or answer == "c" or answer == "d"):
            if (correct_answer == q[ord(answer) - 96]):
                if (lvl == 14):
                    print((" ******* CONGRATULATIONS, %s! *************" % player.upper()))
                    print((" **********  YOU WON $1,000,000! *************"))
                    print((" You reached the top! This was an excellent game! Once again, congratulations!"))
                else:
                    print(("\n You got it right, %s!\n You now have $%s.\n Let's proceed to question #%s!" % (player, balance[lvl + 1], lvl + 2)))
                    print(ask_question(lvl + 1))
                    check_answer(lvl + 1)

            else:
                print(("\n Ups. The answer you chose is incorrect.\n The right answer is %s." % correct_answer))
                print((" Thank you for the game!"))

                user_choice = input("\n\n Would you like to to try one more time? (y/n)   ")
                if (user_choice.lower() == "y"):
                    help_audience_avail = True
                    help_50_avail = True
                    help_friend_avail = True
                    print(ask_question(0))
                    check_answer(0)


    balance = [0, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
    level = 0  # Current question number
    correct_answer = ""
    q = []
    acceptable_answers = ["a", "b", "c", "d", "50", "help", "audience", "friend", "finish"]
    help_50 = "to use \"50:50\", enter '50'"
    help_50_avail = True
    help_friend = "to \"Phone a Friend\", enter 'friend'"
    help_friend_avail = True
    help_audience = "to \"Ask the Audience\", enter 'audience'"
    help_audience_avail = True

    # MAIN
    print(" *************************************************")
    print(" *                AI LÀ TRIỆU PHÚ                *")
    print(" *************************************************\n")

    player = input("Nhập tên của bạn? ")

    print(("\n Hãy bắt đầu trò chơi, %s! Sẽ có 15 câu hỏi\n"
        " được sắp xếp theo độ khó. Các câu hỏi đơn giản hơn\n"
        " đi trước và có giá trị thấp hơn. Mỗi câu hỏi sẽ có bốn \n"
        " các lựa chọn trả lời, trong đó chỉ có một lựa chọn đúng. Trả lời khó nhất,\n"
        " Câu hỏi thứ 15, bạn sẽ giành được 1.000.000 USD! \n\n"
        " Hãy nhớ rằng bạn có 3 sự trợ giúp:\n"
        " %s\n"
        " %s\n"
        " %s\n\n"
        " Bạn luôn có thể nhập 'trợ giúp' để được nhắc về các tùy chọn này.\n\n"
        " Hãy bắt đầu nào!\n"
        % (player, help_50, help_friend, help_audience)))

    print(ask_question(0))
    check_answer(0)

