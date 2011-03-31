import state
import translate

def index():
    return open("index.html").read(), "text/html"

def poll(uuid, lang=""):
    if uuid in state.SW:
        user = state.SW[uuid]
        queue = user.queue

        if lang:
            user.lang = lang

        try:
            return "msg\n"+queue.get(block=False), "text/plain"
        except state.Empty:
            return "none", "text/plain"
    else:
        next_single = state.SINGLE.get(block=False)
        if uuid not in next_single:
            state.SW[uuid] = state.User(next_single[0])
            state.SW[next_single[0]] = state.User(uuid)
            print "poll: Pairing {0} and {1}".format(uuid, next_single[0])
        else:
            state.SINGLE.put(next_single)
        return "wait", "text/plain"

def push(uuid, text="", lang=""):
    user = state.SW[uuid]
    other = state.SW[user.other]

    translated = translate.translate(text, user.lang, other.lang)

    other.queue.put(translated)
    if lang:
        user.lang = lang
    return translated, "text/plain"

def logon():
    import uuid
    new_uuid = str(uuid.uuid4())
    print new_uuid, "signed on"
    if state.SINGLE.empty():
        print "logon: Empty SINGLE, adding to queue"
        state.SINGLE.put((new_uuid, None))
        return new_uuid, "text/plain"
    else:
        other, _ = state.SINGLE.get()
        print "logon: Pairing {0} and {1}".format(new_uuid, other)
        state.SW[new_uuid] = state.User(other)
        state.SW[other] = state.User(new_uuid)
        return new_uuid, "text/plain"

def quit(uuid):
    user = state.SW[uuid]
    other = state.SW[user.other]

    other.queue.put(translate.translate("Your partner has disconnected.", user.lang, other.lang))
    return "quit", "text/plain"

