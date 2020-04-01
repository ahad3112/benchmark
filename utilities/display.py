import sys


class Display:
    line_length = 170
    what_length = 120
    info_length = line_length - what_length

    @staticmethod
    def line(*, line):
        print('{0!s:^{1}}'.format(line, Display.line_length))

    @staticmethod
    def title(*, title):
        print('{0}'.format('-' * Display.line_length))
        print('{0!s:^{1}}'.format(' '.join(x.upper() for x in title), Display.line_length))
        print('{0}'.format('-' * Display.line_length))

    @staticmethod
    def info(*, what, info, fill='>'):
        print('{0:{1}<{2}}{3:{4}>{5}}'.format(what,
                                              fill,
                                              Display.what_length,
                                              info.upper(),
                                              fill,
                                              Display.info_length)
              )

    @staticmethod
    def warning(*, what, info, fill='>'):
        print('{0:{1}<{2}}{3:{4}>{5}}'.format(what,
                                              fill,
                                              Display.what_length,
                                              info.upper(),
                                              fill,
                                              Display.info_length)
              )

    @staticmethod
    def error(*, what, info, fill='>'):
        sys.stderr.write('{0:{1}<{2}}{3:{4}>{5}}'.format(what,
                                                         fill,
                                                         Display.what_length,
                                                         info.upper(),
                                                         fill,
                                                         Display.info_length)
                         )

        sys.stderr.write('\n')

    @staticmethod
    def dataframe(*, headers, rows):
        try:
            # Extra one is required for row number
            min_column_width = Display.line_length // (len(headers) + 1)
        except Exception:
            try:
                # Extra one is required for row number
                min_column_width = Display.line_length // (len(rows[0]) + 1)
            except Exception:
                print('No Header of Data was provided for display.....')
        finally:
            remaining_line_width = Display.line_length - min_column_width
            column_format = '{0!s:{1}<{2}}'
            headers.insert(0, 'No.')
            # headers
            for header in headers:
                print(column_format.format(header, '', min_column_width), end='')
            print()

            # headers underline
            for header in headers:
                print(column_format.format('=' * len(header), '', min_column_width), end='')
            print()

            # printing the row data
            for (index, row) in enumerate(rows):
                print(column_format.format(index, '', min_column_width), end='')
                for column in row:
                    print(column_format.format(column[:min_column_width + 1], '', min_column_width), end='')
                print('\r')

        print('\n** Some column might have been truncated to fit in the column width.')
