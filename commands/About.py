import tools.CommandSystem as command_system
from tools.CommandResult import CommandResult



def about(id, text):
    data = "<b>Цветочный мир</b> - это интернет-магазин с возможностью заказа букетов и цветов онлайн и оформлением доставки " \
           "по Брянску и области.\n\n" \
"<i>У нас вы сможете подобрать букет или цветочную композицию на любой вкус и кошелек. Мы изучили вкусы наших потребителей, " \
           "и рады составлять те композиции, которые гарантированно обрадуют вас и ваших близких!</i> \n\n" \
u"⏰ График работы: <b>круглосуточно</b> \n\n" \
u"\U0001F3E0 Юридический адрес: <b>Россия, г. Брянск, ул. Пушкина, д. 38.</b> \n\n"\
u"\U00002709 Адрес электронной почты: <b>flowersworld@mail.ru</b> \n\n"\
u"\U0000260E По всем вопросам обращаться по телефону: <b>8 (800) 741-23-44</b> \n\n"\
u"\U0001F310 Адрес сайта: <b>https://wp-flowers.ru/</b>"
    result = CommandResult(data)
    return result


about_command = command_system.Command()

about_command.keys = ['о нас', 'about', u'\U00002139 О нас', u'\U00002139 о нас']
about_command.description = 'Информация'
about_command.process = about
