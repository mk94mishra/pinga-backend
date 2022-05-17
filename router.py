from project import project


#user router
from endpoint.user import router as user_router
project.include_router(user_router)

#user router
from endpoint.consult import router as consult_router
project.include_router(consult_router)

#mood router
from endpoint.mood import router as mood_router
project.include_router(mood_router)

#task router
from endpoint.task import router as task_router
project.include_router(task_router)

#issue router
from endpoint.issue import router as issue_router
project.include_router(issue_router)

#subscribe router
from endpoint.subscribe import router as subscribe_router
project.include_router(subscribe_router)

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


#health report router
from endpoint.health import router as health_router
project.include_router(health_router)

#blog report router
from endpoint.blog import router as blog_router
project.include_router(blog_router)
#result router
from endpoint.result import router as result_router
project.include_router(result_router)

#monitor report router
from endpoint.monitor import router as monitor_router
project.include_router(monitor_router)



#monitor report router
from endpoint.mylocal import router as mylocal_router
project.include_router(mylocal_router)







