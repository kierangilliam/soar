simple_move_to_food_agent = """
sp {propose*move-to-food
   (state <s> ^io.input-link.location.<dir>.content 
                 << normalfood bonusfood >>)
-->
   (<s> ^operator <o> + =)
   (<o> ^name move-to-food
        ^direction <dir>)}

sp {apply*move-to-food
   (state <s> ^io.output-link <ol>
              ^operator <o>)
   (<o> ^name move-to-food
        ^direction <dir>)
-->
   (<ol> ^move.direction <dir>)}

sp {apply*move-to-food*remove-move
   (state <s> ^io.output-link <ol>
              ^operator.name move-to-food)
   (<ol> ^move <move>)
   (<move> ^status complete)
-->
   (<ol> ^move <move> -)}
"""

simple_move_to_food_with_monitoring = simple_move_to_food_agent + """
sp {eater*monitor*directions
    (state <s> ^io.input-link.location.<dir>.content <item>)
-->
    (write (crlf) <dir> | <<<<has item>>>> | <item>)}
"""
