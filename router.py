from project import project


#user router
from endpoint.user import router as user_router
project.include_router(user_router)

#mood router
from endpoint.mood import router as mood_router
project.include_router(mood_router)

#task router
from endpoint.task import router as task_router
project.include_router(task_router)

#issue router
from endpoint.issue import router as issue_router
project.include_router(issue_router)

#post router
from endpoint.post import router as post_router
project.include_router(post_router)

#extra router
from endpoint.extra import router as extra_router
project.include_router(extra_router)

#stock router
from endpoint.stock import router as stock_router
project.include_router(stock_router)

#address router
from endpoint.address import router as address_router
project.include_router(address_router)

#form router
from endpoint.form import router as form_router
project.include_router(form_router)

#question router
from endpoint.question import router as question_router
project.include_router(question_router)

#option router
from endpoint.option import router as option_router
project.include_router(option_router)

#answer router
from endpoint.answer import router as answer_router
project.include_router(answer_router)

#result router
from endpoint.result import router as result_router
project.include_router(result_router)

#monitor report router
from endpoint.monitor import router as monitor_router
project.include_router(monitor_router)





