import tempfile
import os


def get_tmp_path():
    tf = tempfile.NamedTemporaryFile()
    print(tf.name)
    filename = tf.name.rindex("\\")
    name = tf.name[filename + 1:len(tf.name)]
    cwd = os.getcwd()
    return cwd + "\\tmp\\" + name + ".pdf"
