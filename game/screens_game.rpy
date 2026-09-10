## Extra screens for the dating loop.

screen aff_hud():
    zorder 90

    frame:
        xpos 18
        ypos 18
        background "#07161ae6"
        padding (14, 10)

        hbox:
            spacing 10
            text "♥ Zim" color "#ff9f1c" size 18
            bar:
                value AnimatedValue(zim_aff, 22, 0.25)
                range 22
                xmaximum 150
                ymaximum 14
                left_bar "#2ec4b6"
                right_bar "#1a3333"
            text "[zim_aff]" color "#2ec4b6" size 18


screen day_map():
    modal True
    add "bg street"
    add Solid("#00000099")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 560
        background "#07161af2"
        padding (32, 28)

        vbox:
            spacing 12
            xfill True

            text "Day [day]" color "#ff9f1c" size 22 xalign 0.5
            text "Where do you look for Zim?" color "#2ec4b6" size 30 xalign 0.5
            text "Pick a place. He will be there. He is always there." color "#c8d6e5" size 16 xalign 0.5

            null height 8

            textbutton "Zim's Base" action Return("base") xalign 0.5
            textbutton "The Dead Park" action Return("park") xalign 0.5
            textbutton "Neon Taco Stand" action Return("taco") xalign 0.5
            textbutton "Learning Cube (outside)" action Return("skool") xalign 0.5
