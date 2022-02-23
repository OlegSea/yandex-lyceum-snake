import pygame, random, time, os

width = 1280
height = 720
if not os.path.exists("record.txt"):
    with open("record.txt", "w") as f:
        f.write(str(0))

leftBorder = 40
rightBorder = 80
upBorder = 40
downBorder = 160

fieldWidth = 1280 - leftBorder - rightBorder
fieldHeight = 720 - upBorder - downBorder

gameWidth = fieldWidth // 40
gameHeight = fieldHeight // 40

random.seed(version=2)

pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((width, height))
pygame.font.init()
myfont = pygame.font.SysFont("Cascadia Mono", 30)
myfont2 = pygame.font.SysFont("Cascadia Mono", 50)
myfont3 = pygame.font.SysFont("Cascadia Mono", 75)
myfont4 = pygame.font.SysFont("Cascadia Mono", 17)
pickup = pygame.mixer.Sound("resources/pickup.wav")
death = pygame.mixer.Sound("resources/death.wav")

pygame.display.set_caption("Snakey")

clock = pygame.time.Clock()

area = pygame.Rect(100, 150, 500, 150)
area0 = pygame.Rect(350, 150, 500, 150)

areaArcade = pygame.Rect(480, 310, 245, 90)

snakeWidth = 40
snakeHeight = 40
x = gameWidth // 2
y = gameHeight // 2
speed = 1
direction = 0
dt = 0
speedCount = 1
req = 100

run = True

keys = pygame.key.get_pressed()
inputBuffer = []

tailX = [0]
tailY = [0]
nTail = 0
prevX = tailX[0]
prevY = tailY[0]
prev2X = 0
prev2Y = 0
isGameover = False
isRun = False

arcadeMode = False

j = 0
while j < 201:
    tailX.append(0)
    tailY.append(0)
    j += 1

fruitX = random.randint(1, gameWidth - 1)
fruitY = random.randint(1, gameHeight - 1)

score = 0

with open("record.txt", "r") as f:
    best = int(f.read())
fruitCount = score / 10


def draw():
    global x, y, speed, snakeHeight, snakeWidth, keys, direction, score, fruitX, fruitY, fruitCount, win, text, prevX, prevY, prev2X, prev2Y, best
    win.fill((102, 102, 102))
    pygame.draw.rect(
        win,
        (80, 80, 80),
        (leftBorder, upBorder, width - rightBorder, height - downBorder),
    )

    pygame.draw.rect(
        win,
        (114, 224, 114),
        pygame.Rect(
            round(x * 40 + leftBorder),
            round(y * 40 + upBorder),
            snakeWidth,
            snakeHeight,
        ),
    )

    k = 0
    while k < nTail:
        pygame.draw.rect(
            win,
            (255, 255, 255),
            pygame.Rect(
                round(tailX[k] * 40 + leftBorder),
                round(tailY[k] * 40 + upBorder),
                snakeWidth,
                snakeHeight,
            ),
        )
        k += 1

    pygame.draw.rect(
        win,
        (224, 114, 114),
        pygame.Rect(
            (fruitX * 40 + leftBorder),
            (fruitY * 40 + upBorder),
            snakeWidth,
            snakeHeight,
        ),
    )
    pygame.draw.rect(
        win,
        (255, 255, 255),
        (leftBorder, upBorder, width - rightBorder, height - downBorder),
        4,
    )

    text = myfont.render("Your score:" + str(score), False, (255, 255, 255))
    win.blit(text, (0 + leftBorder, height - downBorder // 2))
    textRecord = myfont.render("Your best result:" + str(best), False, (255, 255, 255))
    win.blit(textRecord, (0 + leftBorder, height - downBorder // 2 + upBorder))

    pygame.display.update()


def inputCheck():
    global x, y, speed, snakeHeight, snakeWidth, keys, direction, run
    for event in pygame.event.get():
        if event.type == pygame.quit:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                inputBuffer.append(1)
            elif event.key == pygame.K_RIGHT:
                inputBuffer.append(3)
            elif event.key == pygame.K_UP:
                inputBuffer.append(2)
            elif event.key == pygame.K_DOWN:
                inputBuffer.append(4)


def logic():
    global x, y, speed, snakeHeight, snakeWidth, keys, direction, score, fruitX, fruitY, fruitCount, speedCount, req, nTail, tailX, tailY, prevX, prevY, isGameover

    i = 0
    speedCount += dt
    if speedCount >= req:
        speedCount = 1

        prevX = tailX[0]
        prevY = tailY[0]
        tailX[0] = x
        tailY[0] = y
        n = 1
        while n < nTail:
            prev2X = tailX[n]
            prev2Y = tailY[n]
            tailX[n] = prevX
            tailY[n] = prevY
            prevX = prev2X
            prevY = prev2Y
            n += 1

        if inputBuffer:
            direction = inputBuffer[0]
            inputBuffer.pop(0)

        if direction == 1:
            x -= speed

        elif direction == 2:
            y -= speed

        elif direction == 3:
            x += speed

        elif direction == 4:
            y += speed

    if x == fruitX and round(y) == fruitY:
        score += 10
        pickup.play()
        fruitX = random.randint(1, gameWidth - 1)
        fruitY = random.randint(1, gameHeight - 1)
        for i in range(len(tailX)):
            if fruitX == tailX[i]:
                fruitX = random.randint(1, gameWidth - 1)
        for i in range(len(tailY)):
            if fruitY == tailY[i]:
                fruitY = random.randint(1, gameHeight - 1)
        nTail += 1
    if x < 0:
        if arcadeMode == True:
            x = gameWidth
        else:
            isGameover = True
    if x >= gameWidth + 1:
        if arcadeMode == True:
            x = 0
        else:
            isGameover = True
    if y < 0:
        if arcadeMode == True:
            y = gameHeight - 1
        else:
            isGameover = True
    if y >= gameHeight + 1:
        if arcadeMode == True:
            y = 0
        else:
            isGameover = True

    m = 1
    while m < nTail:
        if x == tailX[m] and y == tailY[m]:
            isGameover = True
        m += 1


def gameOver():
    global x, y, speed, snakeHeight, snakeWidth, keys, direction, score, fruitX, fruitY, fruitCount, speedCount, req, nTail, tailX, tailY, prevX, prevY, isGameover, f, best
    death.play()
    while isGameover:
        win.fill((80, 80, 80))
        gameOverTitle = myfont2.render("Game Over!", False, (224, 114, 114))
        win.blit(gameOverTitle, (width // 3, 60))

        pygame.draw.line(win, (255, 255, 255), (100, 150), (500, 150), 4)
        pygame.draw.line(win, (255, 255, 255), (100, 150), (100, 300), 4)
        pygame.draw.line(win, (255, 255, 255), (500, 300), (100, 300), 4)
        pygame.draw.line(win, (255, 255, 255), (500, 150), (500, 300), 4)

        textReset = myfont2.render("Reset", False, (255, 255, 255))
        win.blit(textReset, (120, 220))
        if int(best) < score:
            textScore = myfont.render(
                "Your score:" + str(score) + "(New Record!)", False, (255, 255, 255)
            )
        else:
            textScore = myfont.render(
                "Your score:" + str(score), False, (255, 255, 255)
            )
        textFruits = myfont.render(
            "Eaten fruits:" + str(score // 10), False, (255, 255, 255)
        )
        win.blit(textScore, (width // 2, 150))
        win.blit(textFruits, (width // 2, 200))

        if int(best) < score:
            f.close()
            f = open("record.txt", "w")
            f.write(str(score))
            f.close()

        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        for i in pygame.event.get():
            if (
                i.type == pygame.KEYDOWN
                and i.key == pygame.K_SPACE
                or i.type == pygame.MOUSEBUTTONDOWN
                and i.button == 1
                and area.collidepoint(i.pos)
            ):
                gameOver = False
                x = gameWidth // 2
                y = gameHeight // 2
                speed = 1
                direction = 0
                speedCount = 1
                req = 100

                tailX = [0]
                tailY = [0]
                nTail = 0
                prevX = tailX[0]
                prevY = tailY[0]
                prev2X = 0
                prev2Y = 0
                isGameover = False
                j = 0
                while j < 201:
                    tailX.append(0)
                    tailY.append(0)
                    j += 1

                fruitX = random.randint(1, gameWidth - 1)
                fruitY = random.randint(1, gameHeight - 1)  # Same thing

                score = 0
                fruitCount = score / 10
                f = open("record.txt", "r")
                best = f.read()
                if best == "":
                    best = 0
                    f.close()
                    f = open("record.txt", "w")
                    f.write("0")
                    f.close()


while run:
    dt = clock.tick(240)
    if isRun == False:
        win.fill((80, 80, 80))
        pygame.draw.rect(win, (255, 255, 255), area0, 4)
        pygame.draw.rect(win, (255, 255, 255), pygame.Rect(480, 310, 245, 90), 4)
        textPlay = myfont2.render("Play", False, (255, 255, 255))
        textPlayArcade = myfont.render("Play Arcade", False, (255, 255, 255))
        textLabel = myfont3.render("Snakey", False, (0, 255, 0))
        win.blit(textPlay, (370, 220))
        win.blit(textPlayArcade, (490, 360))
        win.blit(textLabel, (width // 2 - width // 5 + 50, 30))
        pygame.display.update()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif (
                i.type == pygame.KEYDOWN
                and i.key == pygame.K_SPACE
                or i.type == pygame.MOUSEBUTTONDOWN
                and i.button == 1
                and area0.collidepoint(i.pos)
            ):
                textPlay = myfont2.render("Play", False, (0, 255, 0))
                win.blit(textPlay, (370, 220))
                pygame.display.update()
                pygame.time.wait(250)
                isRun = True
            elif (
                i.type == pygame.KEYDOWN
                and i.key == pygame.K_SPACE
                or i.type == pygame.MOUSEBUTTONDOWN
                and i.button == 1
                and areaArcade.collidepoint(i.pos)
            ):
                textPlayArcade = myfont.render("Play Arcade", False, (0, 255, 0))
                win.blit(textPlayArcade, (490, 360))
                pygame.display.update()
                arcadeMode = True
                pygame.time.wait(250)
                isRun = True
            elif i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                run = False
    if isRun == True:
        if isGameover != True:
            draw()
            inputCheck()
            logic()
        if isGameover:
            gameOver()
        if keys[pygame.K_ESCAPE]:
            run = False

pygame.quit()
