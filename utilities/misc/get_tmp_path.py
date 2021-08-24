# import tempfile
import os


def get_tmp_path():
    # tf = tempfile.NamedTemporaryFile()
    try:
        # filename = tf.name.rindex("\\")
        # name = tf.name[filename + 1:len(tf.name)]
        name = "upload"
        cwd = os.getcwd()
        return cwd + "\\tmp\\" + name + ".pdf"
    except:
        # For heroku
        # filename = tf.name.rindex("/")
        # name = tf.name[filename + 1: len(tf.name)]
        name = "upload"
        return "/tmp/" + name + ".pdf"
