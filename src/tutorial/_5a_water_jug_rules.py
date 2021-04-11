"""Water jug rules used in 5a"""

initialize_water_jug = """
sp {water-jug*apply*initialize-water-jug
    (state <s> ^operator <o>)
    (<o> ^name initialize-water-jug)
-->
    (<s> ^name water-jug ^jug <j1>
         ^jug <j2>) 
    (<j1> ^volume 5
          ^contents 0) 
    (<j2> ^volume 3
          ^contents 0)}
"""

initialize_goal_state = """
sp {water-jug*apply*initialize*create*desired-state 
    (state <s> ^operator.name initialize-water-jug) 
-->
    (<s> ^desired.jug <k>)
    (<k> ^volume 3 ^contents 1)}
"""

elaborate_empty_jug = """
sp {water-jug*elaborate*empty 
    (state <s> ^name water-jug
               ^jug <j>) 
    (<j> ^volume <v>
         ^contents <c>) 
-->
    (<j> ^empty (- <v> <c>))}

"""

propose_initialize_water_jug = """
sp {water-jug*propose*initialize-water-jug
    (state <s> ^superstate nil)
   -(<s> ^name)
-->
    (<s> ^operator <o> +)
    (<o> ^name initialize-water-jug)}
"""

propose_empty_indifferent = """
sp {water-jug*propose*empty 
    (state <s> ^name water-jug
               ^jug <j>) 
    (<j> ^contents > 0)
-->
    (<s> ^operator <o> + =) 
    (<o> ^name empty
         ^empty-jug <j>)}         
"""

propose_pour_indifferent = """
sp {water-jug*propose*pour 
    (state <s> ^name water-jug
            ^jug <i>
            ^jug { <j> <> <i> })
    (<i> ^contents > 0)
    (<j> ^empty > 0)
-->
    (<s> ^operator <o> + =) 
    (<o> ^name pour
         ^empty-jug <i> 
         ^fill-jug <j>)}
"""

propose_fill_indifferent = """
sp {water-jug*propose*fill 
    (state <s> ^name water-jug
               ^jug <j>) 
    (<j> ^empty > 0)
-->
    (<s> ^operator <o> + =)
    (<o> ^name fill
         ^fill-jug <j>)}
"""

apply_empty = """
sp {water-jug*apply*empty 
    (state <s> ^name water-jug
               ^operator <o>
               ^jug <j>) 
    (<o> ^name empty
         ^empty-jug <j>) 
    (<j> ^volume <volume>
         ^contents <contents>) 
-->
    # Compact way to create and delete in one identifier
    (<j> ^contents 0
         ^contents <contents> -)}
"""

apply_fill = """
sp {water-jug*apply*fill 
    (state <s> ^name water-jug
               ^operator <o> ^jug <j>)
    (<o> ^name fill ^fill-jug <j>)
    (<j> ^volume <volume> ^contents <contents>)
-->
    (<j> ^contents <volume>)
    (<j> ^contents <contents> -)}
"""

apply_pour__will_empty_jug = """
sp {water-jug*apply*pour*will-empty-empty-jug 
    (state <s> ^name water-jug
               ^operator <o>) 
    (<o> ^name pour
         ^empty-jug <source>
         ^fill-jug <dest>) 
    (<dest> ^volume <dest-volume>
            ^contents <dest-contents>
            ^empty <dest-empty>) 
    # Main condition to test
    (<source> ^volume <source-vol>
              ^contents { <source-contents> <= <dest-empty> }) 
-->
    (<source> ^contents 0 ^contents <source-contents> -)
    (<dest> ^contents (+ <dest-contents> <source-contents>) ^contents <dest-contents> -)}
"""


apply_pour__wont_empty_jug = """
sp {water-jug*apply*pour*will-not-empty-empty-jug 
    (state <s> ^name water-jug
               ^operator <o>) 
    (<o> ^name pour
         ^empty-jug <source>
         ^fill-jug <dest>)
    # Main condition to test
    (<source> ^volume <source-vol>
              ^contents { <source-contents> > <dest-empty> })
    (<dest> ^volume <dest-vol>
            ^contents <dest-con>
            ^empty <dest-empty>)
-->
    (<source> ^contents (- <source-contents> <dest-empty>) 
              ^contents <source-contents> -)
    # Update destination jug's contents to be it's capacity
    (<dest> ^contents <dest-vol> 
            ^contents <dest-con> -)}
"""

detect_goal_state = """
sp {water-jug*detect*goal*achieved 
    (state <s> ^name water-jug
               ^desired.jug <desired>
               ^jug <j>) 
    (<j>       ^volume <v> ^contents <c>)
    (<desired> ^volume <v> ^contents <c>)
-->
    (write (crlf) |The problem has been solved.|) 
    (halt)}
"""
