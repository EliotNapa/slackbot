#coding: UTF-8
import re
import urllib.parse
from xml.sax.saxutils import unescape
from slackbot.bot import listen_to
from ircbot.iso2022encx import Iso2022jpEncX

@listen_to('.+$')
def hello_send(message):
    """
    send slack messeget to irc
    """
    msg_str = Iso2022jpEncX.regularize('{0}'.format(message.body['text']))
    msg_str = url_convert(msg_str)
    user_str = Iso2022jpEncX.regularize('{0}'.format(message.body['username']))

    #send_str = unescape(user_str), unescape(msg_str)
    rest_str = unescape(msg_str)

    send_usr_str = unescape(user_str)
    send_usr_len = len(send_usr_str)

    lest_str_len = len(rest_str)

    index = 0
    while len(rest_str.encode('utf-8')) > 512 - (send_usr_len + 50):
        rest_str = rest_str[0:lest_str_len - index]
        index += 1        

    #send_str = send_usr_str, rest_str

    message._client.irc_bot.send_to_irc(send_usr_str, rest_str)
    #message._client.irc_bot.send_to_irc('({1}) {0}'.format(message.body['text'], message.body['username']))
    #message.send('{0} {1}!'.format(message.body['text'], message.body['username']))



def url_convert(src_string):
    """
    encode last path of url
    """

    result = src_string
    match = re.search(r'<ht.+\|ht.+>',src_string)

    if match:
        result = re.findall(r'<ht.+\|(ht.+)>',src_string)
        result = '<' + result[0] + '>'

    match_enc = re.search(r'<http.+\/\/.+>',result)

    Encode_Path_only = True

    if match_enc:
        if Encode_Path_only:
            fragment_pos = result.rfind('#')

            work_src = result[:-1]
            fragment_part = ''
            if 0 < fragment_pos:
                fragment_part = work_src[fragment_pos:]
                work_src = work_src[:fragment_pos]

            param_part = ''
            param_pos = work_src.rfind('?')
            if 0 < param_pos:
                param_part = work_src[param_pos:]
                work_src = work_src[:param_pos]

            path_part = ''
            path_pos =  work_src.rfind('/')
            if 0 < path_pos:
                path_part = urllib.parse.unquote(work_src[path_pos:])
                path_part = urllib.parse.quote(path_part)
                work_src = work_src[:path_pos]
            result = work_src + path_part + param_part + fragment_part + '>'
        else:
            find_pos = result.find('://')
            if 0 < find_pos:
                result = '<{0}://{1}>'.format(
                        result[1:find_pos],
                        urllib.parse.quote(result[find_pos+3:-1])
                    )

    return result
