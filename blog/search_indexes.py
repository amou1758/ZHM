from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    
"""
每个索引里面必须有且只能有一个字段为 document=True，这代表 django haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)。注意，如果使用一个字段设置了document=True，则一般约定此字段名为text，这是在 SearchIndex 类里面一贯的命名，以防止后台混乱，当然名字你也可以随便改，不过不建议改。

并且，haystack 提供了use_template=True 在 text 字段中，这样就允许我们使用数据模板去建立搜索引擎索引的文件，说得通俗点就是索引里面需要存放一些什么东西，例如 Post 的 title 字段，这样我们可以通过 title 内容来检索 Post 数据了。举个例子，假如你搜索 Python ，那么就可以检索出 title 中含有 Python 的Post了，怎么样是不是很简单？数据模板的路径为 templates/search/indexes/youapp/\<model_name>_text.txt（例如 templates/search/indexes/blog/post_text.txt），其内容为：
templates/search/indexes/blog/post_text.txt

{{ object.title }}
{{ object.body }}
这个数据模板的作用是对 Post.title、Post.body 这两个字段建立索引，当检索的时候会对这两个字段做全文检索匹配，然后将匹配的结果排序后作为搜索结果返回。

"""