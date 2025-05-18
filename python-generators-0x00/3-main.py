#! ../venv/bin/python3.8

import sys
lazy_paginator = __import__('2-lazy_paginate')

try:
    lazy_paginator.paginate_users(100,0)
except BrokenPipeError:
    sys.stderr.close()