from ..base import BaseConverter

class Converter(BaseConverter):
"""
Moline docs have DRAFT watermarks. These can be removed by 
running the following which removes all characters which a unusually 
large fontsize.

```
page_ = page.filter(lambda x: x['bottom'] - x['top'] < 100)
```

"""