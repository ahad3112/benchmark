class Display:
    line_length = 130
    what_length = 100
    info_length = line_length - what_length

    @staticmethod
    def title(*, title):
        print('{0}'.format('-' * Display.line_length))
        print('{0!s:^{1}}'.format(title, Display.line_length))
        print('{0}'.format('-' * Display.line_length))

    @staticmethod
    def info(*, what, info):
        print('{0:><{1}}{2:>>{3}}'.format(what, Display.what_length, info, Display.info_length))

    @staticmethod
    def dataframe(*, headers, rows):
        try:
            # Extra one is required for row number
            min_column_width = self.line_width // (len(headers) + 1)
        except Exception:
            try:
                # Extra one is required for row number
                min_column_width = Display.line_width // (len(rows[0]) + 1)
            except Exception:
                print('No Header of Data was provided for display.....')
        finally:
            remaining_line_width = Display.line_width - min_column_width
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
