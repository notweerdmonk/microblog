class PaginatorShim():
    '''
    A dummy pagination object which can be passed to render_pagination from
    bootstrap-flask. It can be modified into a true paginator by uncommenting
    portions of code.
    '''
    def __init__(self, lst, total, page_number, per_page):
        'Uncomment'
        #self._total = len(lst)
        self._total = total
        self._page = page_number
        self._per_page = per_page
        max_page_number = self.total // per_page
        remainder = self.total % per_page
        if remainder > 0:
            max_page_number = max_page_number + 1
        self._pages = max_page_number
        if page_number > max_page_number:
            self._prev_num = page_number - 1
            self._next_num = None
            self._has_prev = True
            self._has_next = False
            self.items = []
        elif page_number < 1:
            self._prev_num = None
            self._next_num = page_number + 1
            self._has_prev = False 
            self._has_next = True
            self.items = []
        else:
            self._prev_num = None if page_number == 1 \
                    else page_number - 1
            self._next_num = None if page_number == max_page_number \
                    else page_number + 1
            self._has_prev = False if page_number == 1 else True
            self._has_next = False if page_number == max_page_number else True
            'Uncomment'
            #start = per_page * (page_number - 1)
            #end = start + per_page
            #if end > self._total:
            #    end = start + remainder
            #self.items = lst[start:end]
            self.items = lst

    @property
    def total(self):
        return self._total

    @property
    def page(self):
        return self._page

    @property
    def pages(self):
        return self._pages

    @property
    def per_page(self):
        return self._per_page

    @property
    def prev_num(self):
        return self._prev_num

    @property
    def next_num(self):
        return self._next_num

    @property
    def has_prev(self):
        return self._has_prev

    @property
    def has_next(self):
        return self._has_next

    def iter_pages(self):
        for p in range(self._pages):
            yield p + 1
