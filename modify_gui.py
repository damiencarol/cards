import json
import sys, time, pygame


def get_card(data, card_number):
    for card in data["territories"]:
        if card["id"] == card_number:
            return card
    return None

def switch_condition(cond):
    if None == cond: return ["rock"]
    if ["rock"] == cond: return ["animal"]
    if ["animal"] == cond: return ["fruit"]
    if ["fruit"] == cond: return ["night"]
    
    if ["night"] == cond: return ["map"]

    if ["map"] == cond: return None

    return None

def draw_cross(screen, x, y, col=(255,125,125), size=16):
    pygame.draw.line(screen, col, (x, y - size), (x, y + size))
    pygame.draw.line(screen, col, (x -16, y), (x + 16, y))


DB_FILE_NAME="data.json"
data = json.load(open(DB_FILE_NAME))

pygame.init()

size = width, height = 640, 480
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

image_map_big = pygame.image.load("img/map2.png")
image_map = pygame.transform.scale_by(image_map_big, 0.5)

image_unk = pygame.image.load("img/unknown.png")
image_unk_small = pygame.transform.scale_by(image_unk, 0.5)

image_fruit_big = pygame.image.load("img/fruit.png")
image_fruit = pygame.transform.scale_by(image_fruit_big, 0.75)
image_rock = pygame.image.load("img/rock2.png")
image_rock_big = pygame.transform.scale_by(image_rock, 2)
image_animal_big = pygame.image.load("img/animal.png")
image_animal = pygame.transform.scale_by(image_animal_big, 0.75)
#ballrect = ball.get_rect()

image_sun = pygame.image.load("img/sun.png")
image_sun_big = pygame.transform.scale_by(image_sun, 2)
image_moon = pygame.image.load("img/moon.png")
image_moon_big = pygame.transform.scale_by(image_moon, 2)

font = pygame.font.SysFont("comicsansms", 32)
font_points = pygame.font.SysFont("comicsansms", 48)

CARD_COLOR_GREEN = (19, 156, 44)
CARD_COLOR_BLUE = (29, 75, 173)
CARD_COLOR_YELLOW = (194, 152, 2)
CARD_COLOR_RED = (220,50,50)

CARD_COLOR_NIGHT = (56, 24, 104)

coord_x = 100
coord_y = 50

card_width = 150
card_height = 150

current_card = 68 # 54

debug = False

should_continue = True
while should_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: should_continue = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            coord_x = pos[0]
            coord_y = pos[1]
        if event.type == pygame.KEYDOWN:
            #print("     - event.key : " + str(event.key))
            #print("     - pygame.key.name(event.key) : " + pygame.key.name(event.key))
            key_name = pygame.key.name(event.key)

            if "q" == key_name: should_continue = False

            if "up" == pygame.key.name(event.key):
                current_card = current_card + 1
                if current_card > 68: current_card = 1
            if "down" == pygame.key.name(event.key):
                current_card = current_card - 1
                if current_card < 1: current_card = 68
            
            if "d" == key_name: debug = not debug

            if "n" == key_name:
                card = {"id": current_card}
                data["territories"].append(card)
            if "p" == key_name:
                if "day" == card.get("phase", "day"): card["phase"] = "night"
                else: del card["phase"]

            if "m" == key_name:
                if card.get("is_map"):
                    card["is_map"] = False
                else:
                    card["is_map"] = True

            if "c" == key_name:
                if "green" == card.get("color"):
                    card["color"] = "yellow"
                elif "yellow" == card.get("color"):
                    card["color"] = "red"
                elif "red" == card.get("color"):
                    card["color"] = "blue"
                elif "blue" == card.get("color"):
                    card["color"] = "green"
                else:
                    card["color"] = "green"
            if "r" == key_name:
                if not card.get("resources"):
                    card["resources"] = ["rock"]
                elif "rock" == card["resources"][0]:
                    card["resources"][0] = "fruit"
                elif "fruit" == card["resources"][0]:
                    card["resources"][0] = "animal"
                elif "animal" == card["resources"][0]:
                    if len(card["resources"]) > 1:
                        card["resources"][0] = "rock"
                    else:
                        card["resources"].pop()
            if "t" == key_name:
                if not card.get("resources"):
                    card["resources"] = ["rock", "rock"]
                elif len(card["resources"]) < 2:
                    card["resources"].append("rock")
                elif "rock" == card["resources"][1]:
                    card["resources"][1] = "fruit"
                elif "fruit" == card["resources"][1]:
                    card["resources"][1] = "animal"
                elif "animal" == card["resources"][1]:
                    if len(card["resources"]) == 1:
                        card["resources"].pop()
                    else:
                        card["resources"][1] = "rock"

            if "[*]" == key_name:
                if "power" not in card:
                    card["power"] = {"points": 1}
                else:
                    if "conditions" not in card["power"]:
                        card["power"]["conditions"] = ["rock"]
                    else:
                        card["power"]["conditions"] = switch_condition(card["power"]["conditions"])

            if "[+]" == key_name:
                if "power" not in card:
                    card["power"] = {"points": 1}
                else:
                    if "points" not in card["power"]:
                        card["power"]["points"] = 1
                    else:
                        card["power"]["points"] = card["power"]["points"] + 1
            if "[-]" == key_name:
                if "power" not in card:
                    card["power"] = {"points": 1}
                else:
                    if "points" not in card["power"]:
                        card["power"]["points"] = 1
                    else:
                        card["power"]["points"] = card["power"]["points"] - 1
                        if 0 == card["power"]["points"]:
                            del card["power"]["points"]

            if "[0]" == key_name:
                if "requirements" not in card:
                    card["requirements"] = ["rock"]
                else:
                    if "rock" == card["requirements"][0]: card["requirements"][0] = "animal"
                    elif "animal" == card["requirements"][0]: card["requirements"][0] = "fruit"
                    elif "fruit" == card["requirements"][0]:
                        if len(card["requirements"]) == 1: del card["requirements"]
                        else: card["requirements"][0] = "rock"
            if "[1]" == key_name:
                if "requirements" not in card:
                    card["requirements"] = ["rock"]
                else:
                    if len(card["requirements"])==1: card["requirements"].append("rock")
                    elif len(card["requirements"])==2:
                        if "rock" == card["requirements"][1]: card["requirements"][1] = "animal"
                        elif "animal" == card["requirements"][1]: card["requirements"][1] = "fruit"
                        elif "fruit" == card["requirements"][1]:
                            card["requirements"].pop()
            if "[2]" == key_name:
                if "requirements" not in card:
                    card["requirements"] = ["rock"]
                else:
                    if len(card["requirements"])==2: card["requirements"].append("rock")
                    elif len(card["requirements"])==3:
                        if "rock" == card["requirements"][2]: card["requirements"][2] = "animal"
                        elif "animal" == card["requirements"][2]: card["requirements"][2] = "fruit"
                        elif "fruit" == card["requirements"][2]:
                            card["requirements"].pop()
            if "[3]" == key_name:
                if "requirements" not in card:
                    card["requirements"] = ["rock"]
                else:
                    if len(card["requirements"])==3: card["requirements"].append("rock")
                    elif len(card["requirements"])==4:
                        if "rock" == card["requirements"][3]: card["requirements"][3] = "animal"
                        elif "animal" == card["requirements"][3]: card["requirements"][3] = "fruit"
                        elif "fruit" == card["requirements"][3]:
                            card["requirements"].pop()

            if "s" == key_name:
                json.dump(data, open(DB_FILE_NAME, "w"), indent=4)
                print("DB saved")

    card = get_card(data, current_card)
    if not card:
        card = {"id": current_card}
        data["territories"].append(card)

    text_card_id = font.render(str(current_card), True, (12, 13, 97))
    text_points = None
    text_conditions = None
    if card.get("power"):
        if card["power"].get("points"):
            text_points = font_points.render(str(card["power"].get("points")), True, (12, 13, 97))
        if card["power"].get("conditions"):
            text_conditions = font_points.render("=", True, (12, 13, 97))

    """
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
"""

    screen.fill(black)

    #screen.blit(ball, ballrect)
    if card:
        coord_phase = (
            coord_x + 8, #(card_width/6) -16, 
            coord_y + 8, #(card_height/6) -16,
        )
        if "day" == card.get("phase", "day"):
            pygame.draw.rect(screen, (176,213,230),(coord_x, coord_y,card_width,card_height//2))
            screen.blit(image_sun_big, coord_phase)
        else:
            pygame.draw.rect(screen, CARD_COLOR_NIGHT,(coord_x, coord_y,card_width,card_height//2))
            screen.blit(image_moon_big, coord_phase)
        card_color = (25,25,25)
        if "green" == card.get("color"):
            card_color = CARD_COLOR_GREEN
        if "red" == card.get("color"):
            card_color = CARD_COLOR_RED
        if "yellow" == card.get("color"):
            card_color = CARD_COLOR_YELLOW
        if "blue" == card.get("color"):
            card_color = CARD_COLOR_BLUE
        pygame.draw.rect(screen, card_color,(
            coord_x, coord_y + (card_height//2),
            card_width, card_height//2))
        # resource 0
        coord_r0 = (
            coord_x + card_width - 16, 
            coord_y + 16,
        )
        # resource 1
        coord_r1 = (
            coord_x + card_width - 24, 
            coord_y + (card_height//6) - 16,
        )
        # resource 2
        coord_r2 = (
            coord_x + card_width - 54, 
            coord_y + (card_height//6) - 16,
        )
        image_r0 = image_unk
        image_r1 = image_unk
        if len(card.get("resources", []))>0:
            if "fruit" == card["resources"][0]: image_r0 = image_fruit
            elif "rock" == card["resources"][0]: image_r0 = image_rock
            elif "animal" == card["resources"][0]: image_r0 = image_animal
        else:
            image_r0 = None
        if len(card.get("resources", []))>1:
            if "fruit" == card["resources"][1]: image_r1 = image_fruit
            elif "rock" == card["resources"][1]: image_r1 = image_rock
            elif "animal" == card["resources"][1]: image_r1 = image_animal
        else:
            image_r1 = None

        c_r0_x = coord_x + card_width - 20
        c_r0_y = coord_y + 20
        c_r1_x = coord_x + card_width - 20 - 32
        c_r1_y = coord_y + 20
        if image_r0:
            screen.blit(image_r0, (c_r0_x - 8, c_r0_y - 8))
            # debug
            if debug:
                pygame.draw.line(screen, (255,125,125), (c_r0_x - 16, c_r0_y), (c_r0_x+16, c_r0_y))
                pygame.draw.line(screen, (255,125,125), (c_r0_x, c_r0_y - 16), (c_r0_x, c_r0_y + 16))
        if image_r1:
            # debug
            if debug:
                pygame.draw.line(screen, (255,125,125), (c_r1_x - 16, c_r1_y), (c_r1_x+16, c_r1_y))
                pygame.draw.line(screen, (255,125,125), (c_r1_x, c_r1_y - 16), (c_r1_x, c_r1_y + 16))
            screen.blit(image_r1, (c_r1_x - 8, c_r1_y - 8))

        if card.get("is_map", False):
            coord_map = (
                coord_x + 32 + 16, 
                coord_y + 16,
            )
            screen.blit(image_map_big, (coord_map[0]-16, coord_map[1]-16))
            if debug: draw_cross(screen, coord_map[0], coord_map[1])
        
        if text_points:
            size_rect_point = 20
            x_calc = coord_x + (card_width // 4)*3 + size_rect_point//2 #- (text_points.get_width() // 2)
            y_calc = coord_y + (card_height // 2) + card_height//4 #+ (card_height // 4) - text_points.get_height() // 2


            # whit rectangle
            pygame.draw.rect(screen, (255,255,255), (x_calc-size_rect_point, y_calc-size_rect_point
                                                     ,size_rect_point*2, size_rect_point*2))
            # debug
            if debug:
                pygame.draw.line(screen, (255,125,125), (x_calc, y_calc - 16), (x_calc, y_calc+16))
                pygame.draw.line(screen, (255,125,125), (x_calc -16, y_calc), (x_calc + 16, y_calc))

            # text points
            screen.blit(text_points, (x_calc - (text_points.get_width() // 2), (y_calc- (text_points.get_height() // 2))))
        
            # equal text
            if text_conditions:
                screen.blit(text_conditions, (x_calc - (text_conditions.get_width() // 2) - size_rect_point*2, (y_calc- (text_conditions.get_height() // 2))))
                # debug
                if debug:
                    pygame.draw.line(screen, (255,125,125), (x_calc - size_rect_point*2, y_calc - 16), (x_calc - size_rect_point*2, y_calc+16))
                    pygame.draw.line(screen, (255,125,125), (x_calc - size_rect_point*2 -16, y_calc), (x_calc - size_rect_point*2 + 16, y_calc))
                
                img_condition = image_unk
                c_x = x_calc - size_rect_point*4
                if ["rock"] == card["power"]["conditions"]: img_condition = image_rock_big
                if ["fruit"] == card["power"]["conditions"]: img_condition = image_fruit_big
                if ["animal"] == card["power"]["conditions"]: img_condition = image_animal_big
                if ["night"] == card["power"]["conditions"]: img_condition = image_moon_big
                if ["map"] == card["power"]["conditions"]: img_condition = image_map_big
                screen.blit(img_condition, (c_x - 16, y_calc - 16))
                if debug:
                    pygame.draw.line(screen, (255,125,125), (c_x, y_calc - 16), (c_x, y_calc+16))
                    pygame.draw.line(screen, (255,125,125), (c_x -16, y_calc), (c_x + 16, y_calc))
            
            for k in range(0,len(card.get("requirements", []))):
                req1_x = coord_x + card_width - 8 - 16*(1+k)
                req1_y = coord_y + card_width//2 - 8
                img_req = image_unk_small
                if "rock" == card["requirements"][k]: img_req = image_rock
                if "animal" == card["requirements"][k]: img_req = image_animal
                if "fruit" == card["requirements"][k]: img_req = image_fruit
                screen.blit(img_req, (req1_x-8, req1_y-8))
                if debug: draw_cross(screen, req1_x, req1_y)


    screen.blit(text_card_id, (
        coord_x + 24 - text_card_id.get_width() // 2,
        coord_y + 24 - text_card_id.get_height() // 2)
    )
    
    if debug:
        color_debug = (255,0,0)
        pygame.draw.line(screen,color_debug, (coord_x, coord_y), (coord_x+card_width, coord_y))
        pygame.draw.line(screen,color_debug, (coord_x+card_width, coord_y), (coord_x+card_width, coord_y+card_height))
        pygame.draw.line(screen,color_debug, (coord_x+card_width, coord_y+card_height), (coord_x, coord_y+card_height))
        pygame.draw.line(screen,color_debug, (coord_x, coord_y+card_height), (coord_x, coord_y))

    time.sleep(0.01)
    pygame.display.flip()
