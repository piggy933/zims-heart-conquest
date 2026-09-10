# Operation Heart Doom — a one-route dating sim.
# Zim uses the player's hand-drawn sprites.

define z = Character("Zim", color="#2ec4b6")
define gir = Character("Gir", color="#ff9f1c")
define comp = Character("BASECORE", color="#ff4d4d")
define mc = Character("[player_name]", color="#c8d6e5")

default player_name = "Alex"
default zim_aff = 0
default day = 1
default visits_base = 0
default visits_park = 0
default visits_taco = 0
default visits_skool = 0

image bg street = "images/bg_street.png"
image bg base = "images/bg_base.png"
image bg park = "images/bg_park.png"
image bg skool = "images/bg_skool.png"
image bg taco = "images/bg_taco.png"
image bg space = "images/bg_space.png"
image bg house = "images/bg_house.png"
image bg menu = "images/bg_menu.png"
image cg love = "images/cg_love.png"
image cg bad = "images/cg_bad.png"

# Feet sit just above the 185px dialogue box (720 - 185 = 535).
define sprite_feet_y = 528

image zim neutral = Transform("images/zim_neutral.png", zoom=1.15, yanchor=1.0, ypos=sprite_feet_y, xalign=0.5)
image zim happy = Transform("images/zim_happy.png", zoom=1.15, yanchor=1.0, ypos=sprite_feet_y, xalign=0.5)
image zim angry = Transform("images/zim_angry.png", zoom=1.15, yanchor=1.0, ypos=sprite_feet_y, xalign=0.5)
image zim flustered = Transform("images/zim_flustered.png", zoom=1.15, yanchor=1.0, ypos=sprite_feet_y, xalign=0.5)
image zim evil = Transform("images/zim_evil.png", zoom=1.15, yanchor=1.0, ypos=sprite_feet_y, xalign=0.5)
image gir = Transform("images/gir.png", zoom=0.45, yanchor=1.0, ypos=sprite_feet_y, xalign=0.78)
image gir right = Transform("images/gir.png", zoom=0.45, yanchor=1.0, ypos=sprite_feet_y, xalign=0.78)
image gir happy = Transform("images/gir_happy.png", zoom=0.45, yanchor=1.0, ypos=sprite_feet_y, xalign=0.78)
image gir happy right = Transform("images/gir_happy.png", zoom=0.45, yanchor=1.0, ypos=sprite_feet_y, xalign=0.78)
image gir angry = Transform("images/gir_angry.png", zoom=0.45, yanchor=1.0, ypos=sprite_feet_y, xalign=0.78)
image gir angry right = Transform("images/gir_angry.png", zoom=0.45, yanchor=1.0, ypos=sprite_feet_y, xalign=0.78)
image gir sad = Transform("images/gir_sad.png", zoom=0.45, yanchor=1.0, ypos=sprite_feet_y, xalign=0.78)
image gir sad right = Transform("images/gir_sad.png", zoom=0.45, yanchor=1.0, ypos=sprite_feet_y, xalign=0.78)

transform zim_left:
    xalign 0.22
    yanchor 1.0
    ypos sprite_feet_y
    zoom 1.15

transform zim_center:
    xalign 0.5
    yanchor 1.0
    ypos sprite_feet_y
    zoom 1.15

# Ren'Py built-ins: easeinleft / easeinright slide the sprite on,
# then vpunch shakes the whole screen.
init python:
    def gir_arrive(name, side="right"):
        enter = easeinright if side == "right" else easeinleft
        renpy.show(name)
        renpy.with_statement(enter)
        renpy.with_statement(vpunch)

init python:
    def bump_aff(n):
        store.zim_aff += n
        if n > 0:
            renpy.notify("Zim's interest rose.")
        elif n < 0:
            renpy.notify("Zim's interest fell.")


label start:
    stop music fadeout 1.0
    play music "illurock.opus" fadein 1.5
    show screen aff_hud

    scene bg house
    with fade

    "The lease was cheap. The neighborhood was uglier. The house next door hummed at night like a microwave plotting revenge."

    $ player_name = renpy.input("Your name? (you are an adult neighbor, 18+)", default="Alex", length=16).strip()
    if player_name == "":
        $ player_name = "Alex"

    "You signed as [player_name]. Boxes everywhere. One lamp. A window that stares at a house that should not exist."

    "A knock. Too fast. Too many knuckles."

    show zim evil
    with dissolve

    z "EARTH-DWELLER. You have moved within BLAST RADIUS of the mighty ZIM."

    z "State your function! Spy? Delivery meat? Inferior roommate species?!"

    menu:
        "How do you answer the tiny green menace in your doorway?"

        "I'm your new neighbor. Try not to explode the street.":
            $ bump_aff(2)
            show zim flustered
            z "The GREAT ZIM does not explode streets. Zim EXPLODES planets. There is a difference, [player_name]."

        "If you're selling something, I already have a vacuum.":
            $ bump_aff(-1)
            show zim angry
            z "INSOLENCE. Zim is not a salesman. Zim is an INVADER. Note the scarf of AUTHORITY."

        "Those antennae are a lot.":
            $ bump_aff(1)
            show zim happy
            z "They are SENSORY SPIRES. Your Earth-hair is the strange part. This pleases Zim. Confusion is useful."

    show zim at zim_left
    with move
    $ gir_arrive("gir happy")

    gir "HELLO NEW MEAT FRIEND. I brought a taco. It is leaking. That means it is ALIVE."

    mc "That's... not how tacos work."

    show gir angry
    gir "Then Earth is WRONG."

    hide gir
    show zim neutral at zim_center
    with dissolve

    z "This is Gir. My assistant. My disaster. Do not teach it manners. Manners are a human virus."

    z "You will report to Zim for INSPECTION tomorrow. Refuse, and I will relocate your house into the sky."

    hide zim
    with dissolve

    "He leaves. The doorframe smokes a little. Gir waves with the taco."

    "You should call the landlord. You make tea instead."

    $ day = 2
    jump day_loop


label day_loop:
    if day > 6:
        jump finale

    scene bg street
    with fade
    $ narrator("Day [day]. The neighbor's house is still humming. Where do you go?", interact=False)

    call screen day_map

    if _return == "base":
        $ visits_base += 1
        call loc_base
    elif _return == "park":
        $ visits_park += 1
        call loc_park
    elif _return == "taco":
        $ visits_taco += 1
        call loc_taco
    elif _return == "skool":
        $ visits_skool += 1
        call loc_skool

    $ day += 1
    jump day_loop


label loc_base:
    scene bg base
    with fade

    if visits_base == 1:
        show zim happy
        z "You CAME. The inspection begins. Stand on the glowing circle. Ignore the screaming."

        "The circle is just a floor lamp with the shade removed. The screaming is a kettle."

        menu:
            "What do you do?"

            "Stand on the circle and play along.":
                $ bump_aff(3)
                show zim flustered
                z "Obedience. Rare in Earth-apes. Zim will... file this under USEFUL."

            "Unplug the kettle first.":
                $ bump_aff(2)
                show zim angry
                z "You silenced my WAR HORN. It was boiling water. That is STILL a war horn."

            "Ask what the red eye on the wall is watching.":
                $ bump_aff(1)
                hide zim
                show zim evil
                comp "BASECORE ONLINE. New organism tagged: [player_name]. Threat level: annoyingly charming."
                show zim angry
                z "STOP FLIRTING WITH MY COMPUTER."

    elif visits_base == 2:
        show zim evil
        z "Today we test COMPATIBILITY. Sit. The chair has only mild electricity."

        menu:
            "Zim holds out two helmets made of colanders."

            "Put the colander on. Match his energy.":
                $ bump_aff(3)
                show zim happy
                z "YES. Dual-brain invasion. Your thoughts are loud. They keep saying 'this is a date.' SILENCE, thoughts."

            "Suggest coffee instead of electrocution.":
                $ bump_aff(2)
                show zim flustered
                z "Coffee is a bean juice. Zim accepts bean juice. Do not call it a date. Call it a BRIEFING."

            "Refuse and inspect his gadgets from a safe distance.":
                $ bump_aff(0)
                show zim angry
                z "Cowardice detected. Also... wisdom. Zim hates when those overlap."

    else:
        show zim flustered
        z "You keep returning to the lair. This is either loyalty or a trap. Zim prefers loyalty. It is warmer."

        menu:
            "The base lights dim to a very unsubtle magenta-orange."

            "Tell him you like being here.":
                $ bump_aff(3)
                show zim happy
                z "THEN STAY. Not forever. Forever is for later. After the briefing. After snacks."

            "Tease him: 'Warmth? From the invader?'":
                $ bump_aff(2)
                show zim angry
                z "THE GREAT ZIM HAS A CORE TEMPERATURE. It is SCIENCE. Stop smiling."

            "Change the subject to world domination.":
                $ bump_aff(1)
                show zim evil
                z "YES. Lists. Spreadsheets of DOOM. You may hold the glitter pen."

    hide zim
    return


label loc_park:
    scene bg park
    with fade

    if visits_park == 1:
        show zim angry
        z "This park is a FAILURE. The swings creak. The ducks are insubordinate."

        menu:
            "A duck stares at Zim. Zim stares back."

            "Sit on the swing next to him.":
                $ bump_aff(2)
                show zim flustered
                z "Earth recreation is primitive. ...Do not stop. The swinging is acceptable."

            "Translate for the duck: he's not a threat, he's dramatic.":
                $ bump_aff(1)
                show zim happy
                z "DRAMATIC is a warrior trait. The duck may live. For now."

            "Suggest leaving before someone calls animal control on an alien.":
                $ bump_aff(-1)
                show zim angry
                z "I AM A NORMAL BOY WITH A SKIN CONDITION AND A SCARF. Say it WITH me."

    elif visits_park == 2:
        show zim neutral
        z "I have packed a picnic. It is tactical rations. And one stolen pastry. For you. Not because of FEELINGS."

        menu:
            "The pastry is slightly singed. It still smells good."

            "Eat it and thank him properly.":
                $ bump_aff(3)
                show zim flustered
                z "Your gratitude is... loud. Zim will allow it. Quietly. Inwardly. AHH I SAID TOO MUCH."

            "Split it with him.":
                $ bump_aff(2)
                show zim happy
                z "Resource sharing. Alliance behavior. Gir is not invited. Gir would eat the plate."

            "Ask if this is a date.":
                $ bump_aff(1)
                show zim angry
                z "It is SURVEILLANCE of a public lawn. With pastry. Stop using Earth words."

    else:
        show zim evil
        "Sunset turns the dead grass almost pretty. Zim pretends he is not watching you."

        menu:
            "The invader's spring-antenna twitches."

            "Lean in and tell him the park is better with him in it.":
                $ bump_aff(3)
                show zim flustered
                z "THEN THE PARK IS A SUCCESSFUL CONQUEST. I mean. The lawn. I mean. Sit closer."

            "Point out a star and ask if his planet is out there.":
                $ bump_aff(2)
                show zim neutral
                z "Vrel is that way. Probably. The maps were drawn in crayon. I was a very confident child-soldier."

            "Stay quiet and watch the sky with him.":
                $ bump_aff(2)
                "He does not speak for a full minute. For Zim, that is a sonnet."

    hide zim
    return


label loc_taco:
    scene bg taco
    with fade

    if visits_taco == 1:
        $ gir_arrive("gir happy")
        gir "TACO NIGHT. Zim said not to invite you. So I invited you TWICE."

        show gir happy right
        show zim angry at zim_left
        with move
        z "Gir. Traitor. Fine. You may observe how Zim consumes Earth cylinders of regret."

        menu:
            "Grease drips. Neon buzzes. This is, somehow, a date."

            "Buy Zim an extra taco. No speech. Just the taco.":
                $ bump_aff(3)
                show zim flustered at zim_left
                z "Tribute. Acceptable. Do not look at me while I enjoy it. Enjoyment is classified."

            "Let Gir order for the table.":
                $ bump_aff(0)
                show gir happy right
                gir "THREE TACOS AND A NAPKIN HAT."
                show zim angry at zim_left
                z "I am wearing the napkin hat under protest."

            "Ask Zim why he hides here instead of the base.":
                $ bump_aff(1)
                show zim evil at zim_left
                z "Because the taco stand has WI-FI and despair. Perfect invasion climate."

    elif visits_taco == 2:
        show zim neutral
        z "Gir is in the dumpster making friends. We have approximately four minutes of peace."

        menu:
            "Four minutes. The neon makes his red eyes look almost soft."

            "Tell him you like the peace, and him in it.":
                $ bump_aff(3)
                show zim flustered
                z "PEACE is a temporary ceasefire of the heart. That is a NORMAL sentence. I read it on a napkin."

            "Offer to help him with the 'invasion' paperwork.":
                $ bump_aff(2)
                show zim happy
                z "YES. You have spreadsheets. Earth is doomed. I am... glad it is you."

            "Joke that Gir is a better date.":
                $ bump_aff(-2)
                show zim angry
                z "TAKE IT BACK. Gir dates TACOS. Zim dates... NOBODY. Especially not you. ESPECIALLY."

    else:
        $ gir_arrive("gir happy")
        gir "Zim practiced saying your name in the mirror. He broke the mirror. Then he taped it back. Then he practiced MORE."

        show zim angry at zim_left
        z "LIES. SLANDER. The mirror attacked FIRST."

        menu:
            "He is the color of a warning light."

            "Say his name back, gently.":
                $ bump_aff(3)
                show zim flustered at zim_left
                z "...Again. Slower. For calibration."

            "Laugh, but kindly.":
                $ bump_aff(1)
                show zim happy at zim_left
                z "Mockery detected. Affection also detected. Confusing. Keep doing both."

            "Change the subject to salsa.":
                $ bump_aff(0)
                z "Salsa is lava for cowards. I respect it."

    hide zim
    return


label loc_skool:
    scene bg skool
    with fade

    if visits_skool == 1:
        show zim evil
        z "Behold: the Learning Cube. I gather intelligence from OUTSIDE. Children are sticky. I do not go in. You do not go in. We are ADULTS with a PLAN."

        "You stay on the sidewalk. The building looks like a prison that failed art class."

        menu:
            "Zim scribbles in a notebook labeled DOOM / SNACKS."

            "Help him sketch a better map of the block.":
                $ bump_aff(2)
                show zim happy
                z "Your lines are straight. Terrifying. Attractive. I will allow the second word internally."

            "Ask why an invader cares about a school he doesn't enter.":
                $ bump_aff(1)
                show zim neutral
                z "Because the Tall Ones used to measure worth in hallways. I measure worth in... other things. Now."

            "Suggest going somewhere less grim.":
                $ bump_aff(0)
                show zim angry
                z "GRIM is my aesthetic. You may hold my notebook anyway."

    elif visits_skool == 2:
        show zim flustered
        z "I brought two visors. We look like city inspectors. No one will question the scarf."

        menu:
            "You look like a very small municipal employee and a confused civilian."

            "Play along and 'inspect' the fence together.":
                $ bump_aff(3)
                show zim happy
                z "PARTNERSHIP. Circle the cracked concrete. Initial here. Your handwriting is... keep writing."

            "Take the visor off him and tell him he doesn't need a costume with you.":
                $ bump_aff(2)
                show zim flustered
                z "WITHOUT the visor I am merely Zim. That is. Fine. Obviously. Stop looking at my eyes."

            "Photograph the ugly building for his files.":
                $ bump_aff(1)
                z "Evidence. Of ugliness. Earth is consistent. You are the exception."

    else:
        show zim neutral
        "After hours. Empty lot. Wind in the chain-link. Zim's antennae twitch like a clock."

        menu:
            "He is quieter than usual."

            "Ask what he wants if the invasion never happens.":
                $ bump_aff(3)
                show zim flustered
                z "Then I would still knock on your door. With fewer threats. Maybe the same number of threats."

            "Offer your hand. No speech.":
                $ bump_aff(3)
                show zim flustered
                "He stares at your hand as if it is a weapon. Then he takes it. His glove is warm."

            "Promise you'll keep his secret.":
                $ bump_aff(2)
                show zim happy
                z "THE SECRET OF ZIM is safe. Also the secret that Zim likes your voice. FORGET THE SECOND SECRET."

    hide zim
    return


label finale:
    scene bg house
    with fade

    "Day seven. The humming next door changes pitch. Like a question."

    $ gir_arrive("gir happy")
    gir "Zim says come to the roof. He practiced a speech. He ate the speech. Then he wrote a new speech on a taco wrapper."

    scene bg space
    with fade

    show zim evil
    z "[player_name]. The briefing is this: Earth is still doomed. Also. I have a second briefing."

    if zim_aff >= 16:
        jump ending_love
    elif zim_aff >= 8:
        jump ending_good
    else:
        jump ending_bad


label ending_love:
    show zim flustered
    z "The second briefing is... HEARTS. Specifically yours. I have decided it is STRATEGIC TERRITORY."

    z "I will not conquer you. That was the old plan. The new plan is worse. It is called sharing a planet. And snacks."

    menu:
        "The stars make his gold eyes look like they finally found a map."

        "Tell him he already has that territory.":
            $ bump_aff(2)
            show zim happy
            z "THEN OPERATION HEART DOOM IS A SUCCESS. Gir, do NOT throw confetti tacos—"

        "Kiss his scarf-knot, because his face is still buffering.":
            $ bump_aff(2)
            show zim flustered
            z "CALIBRATION ERROR. Repeat the experiment. For science. Forever."

    scene cg love
    with fade

    "You stay on the roof until the city looks almost kind. Zim talks about Vrel, then about your lamp, then about nothing, which is how he says plenty."

    z "The Great Zim chooses you. Not as a minion. As the other idiot on the mission."

    "Gir cheers from a gutter. A taco flag waves. It is the worst parade. It is yours."

    "TRUE END — Co-Invaders"

    hide screen aff_hud
    return


label ending_good:
    show zim neutral
    z "The second briefing is alliance. You are not doomed. You are... permitted. Near Zim. On purpose."

    z "I still might conquer the block. You may have visiting hours. And the good chair."

    menu:
        "It is not a confession. It is the closest he can currently build."

        "Accept the alliance. Ask for better visiting hours.":
            $ bump_aff(1)
            show zim happy
            z "NEGOTIATION. Attractive. Midnight to midnight. I am generous."

        "Tell him he can do better than 'permitted' next week.":
            show zim flustered
            z "NEXT WEEK I will use a warmer word. I am researching 'like.' Do not rush SCIENCE."

    scene bg street
    with fade

    "You walk him back to the humming house. He does not explode the street. He waves, once, like it hurts."

    "GOOD END — Uneasy Alliance"

    hide screen aff_hud
    return


label ending_bad:
    show zim angry
    z "The second briefing is evacuation. You are a distraction. Distractions get relocated. Possibly into a hedge."

    z "Zim does not need a neighbor. Zim needs DOOM. You may keep the lamp."

    menu:
        "The portal in the yard coughs orange light."

        "Wish him luck anyway.":
            show zim flustered
            z "...Luck is for people who stay. I am leaving. Stop looking like that."

        "Tell him the door is open if he ever wants a briefing that isn't an exit.":
            show zim angry
            z "I WILL NOT. I might. NO. The portal is THIS way."

    scene cg bad
    with fade

    hide zim
    $ gir_arrive("gir sad")

    "The house stops humming. The street is ordinary and worse. Gir leaves a single cold taco on your step, like an apology in edible form."

    "BAD END — Operation Abandoned"

    hide screen aff_hud
    return
