import numpy

TIME_ID = 5

USERS_NUMB = 35056          # CTHULHU
ITEMS_NUMB = 21825          # CTHULHU

""" section for classic cross-validation """
TRAINING_USERS_RATE = 0.8   # CTHULHU
TRAINING_ITEMS_RATE = 0.8   # CTHULHU
TESTING_USERS_RATE = 1 - TRAINING_USERS_RATE    # CTHULHU
TESTING_ITEMS_RATE = 1 - TRAINING_ITEMS_RATE    # CTHULHU

SWITCHES_USERS_NUMB = int(1 / TESTING_USERS_RATE)   # CTHULHU
SWITCHES_ITEMS_NUMB = int(1 / TESTING_ITEMS_RATE)   # CTHULHU

WINDOW_USERS_SIZE = int(USERS_NUMB / SWITCHES_USERS_NUMB)   # CTHULHU
WINDOW_ITEMS_SIZE = int(ITEMS_NUMB / SWITCHES_ITEMS_NUMB)   # CTHULHU
""" \classic cross-validation """

""" section for special time cross-validation """
#STEPS_NUMB = 11
ITEM_STEP = 2000
ITERATIONS_NUMB = ITEMS_NUMB / ITEM_STEP
""" \special time cross-validation """

MAX_METAS_NUMB = 17
#METAS_TO_USE = {3 : "place", 4 : "presenter", 6 : "category", 9 : "organizer", 11 : "city", 15 : "seminartype"}
METAS_TO_USE = {6 : "categories", 15 : "seminar_types"}
META_WEIGHTS = numpy.array([[0.7], [0.3]], dtype = float)

TIME_TRESHOLD_INTERVAL = 24

""" 	select
	0 - id
	1 - title
	2 - body
	3 - place_id
	4 - presenter_id
	5 - date
	6 - category_id
	7 - visit_conditions
	8 - price
	9 - organizer_id
	10 - publish_at
	11 - city_id
	12 - is_published
	13 - note
	14 - special_offer
	15 - seminar_type_id
	16 - featured
		from theorycopy.seminars where is_published=1;
"""
