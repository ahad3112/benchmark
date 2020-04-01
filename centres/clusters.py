if __name__ != '__main__':
    '''
    I don't want this script to be run as the Top level script
    Should add to other module
    '''
    import os
    import sys
    import settings
    from datetime import date
    from utilities.display import Display

    class ClusterMixin:

        # This will be populated with computed valued in __update_template method
        computed_params = {}

        targets = {
            '$name$': 'replace_arg',
            '$project$': 'replace_arg',
            '$wall_time$': 'replace_arg',
            '$error_file$': 'replace_arg',
            '$output_file$': 'replace_arg',
            '$nodes$': 'replace_arg',
            '$ntasks-per-node$': 'replace_arg',
            '$MPI_NP$': 'replace_arg',
            '$gres$': 'replace_varargs',
            '$modules$': 'replace_varargs',
            '$envs$': 'replace_varargs',
            '$memories$': 'replace_varargs',
            '$exe$': 'set_exe',
            '$simg$': 'set_simg',
            '$threads$': 'set_threads'
        }

        working_directory_created = False

        def __init__(self, *, args):
            self.args = args

            #  housekeeping for storing job script
            self.__housekeeping()
            # load the template
            self.__load_template()
            # Replace target by the user provided value in the template
            self.__update_template()

        def __housekeeping(self):
            Display.title(
                title='Setting Up Working Directory for {0}'.format(self.__class__.__name__)
            )
            try:
                workdir = os.path.abspath(self.args.workdir)
            except Exception:
                raise Exception('No default or user provided Working directory was provided...')
            else:
                if workdir == settings.HOME_DIRECTORY:
                    Display.warning(what='Using program directory as working directory ', info=' [ Warning ]')
                    confirmation = input("Type 'y/Y' to proceed? ")
                    if not confirmation in ['y', 'Y']:
                        Display.error(what='You chose not to proceed ', info=' [ ABORTING ]')
                        sys.exit()

                    if workdir != settings.DEFAULT_WORKDIR:
                        os.chdir(workdir)

                else:
                    if workdir != settings.DEFAULT_WORKDIR:
                        os.chdir(workdir)

            Display.info(what='{0} '.format(workdir), info=' [ Set as Working Dirrectory ]', fill='-')

            #  Creating Directory for the benchmark
            print('\n')
            Display.title(
                title='Creating Benchmark Directory for {0}'.format(self.__class__.__name__)
            )

            self.benchmark_directory = os.path.join(
                os.getcwd(),
                os.path.join(
                    self.args.name,
                    os.path.join(
                        str(date.today()),
                        self.__class__.__name__
                    )
                )
            )

            if os.path.exists(self.benchmark_directory):
                contents_here = os.listdir(self.benchmark_directory)
                if contents_here:
                    Display.info(what='{0} '.format(self.benchmark_directory), info=' [ Directory Not Empty ]', fill='-')
                    confirmation = input("\nType 'o/O' to override, 'b/b' for backup contents and any other key to quit?\n".format(
                        self.benchmark_directory)
                    )

                    if confirmation in ['o', 'O']:
                        # Remove every thing from the directory
                        Display.warning(what='Overriding {0} '.format(self.benchmark_directory), info=' [ Warning ]', fill='-')
                        os.system('rm -rf {0}'.format(
                            os.path.join(self.benchmark_directory, '*'))
                        )
                    elif confirmation in ['b', 'B']:
                        Display.title(title='BACKING UP CONTENTS')
                        Display.info(
                            what='{0} with suffix '.format(os.path.join(self.benchmark_directory, '*')),
                            info=' [ "{0}" ]'.format(
                                settings.DEFAULT_FILE_BACKUP_SUFFIX),
                            fill='-'
                        )
                        # Storing current working directory to get back
                        cwd = os.getcwd()
                        os.chdir(self.benchmark_directory)
                        for content in sorted(contents_here, reverse=True):
                            os.rename(content, content + settings.DEFAULT_FILE_BACKUP_SUFFIX)

                        # going back to the working directory as it was
                        os.chdir(cwd)
                    else:
                        Display.error(what='You chose not to proceed ', info=' [ ABORTING ]')
                        sys.exit()
            else:
                os.system('mkdir -p {0}'.format(self.benchmark_directory))

        def __load_template(self):
            Display.title(
                title='Loading Job Template for {0}'.format(self.__class__.__name__)
            )
            try:
                file = open(
                    os.path.join(
                        settings.TEMPLATE_DIRECTORY,
                        self.__class__.__name__.lower()
                    ),
                    'r'
                )
            except FileNotFoundError:
                raise FileNotFoundError('Template not available for Cluster: {0}.'.format(
                    self.__class__.__name__
                ))
            else:
                Display.info(
                    what='Template ',
                    info=' [ Found ]',
                    fill='-'
                )
                self.template = file.read()

        def replace_arg(self, target, value):
            self.template = self.template.replace(target, value)

        def set_exe(self, target, value):
            self.replace_arg(target, ' '.join(value))

        def set_simg(self, target, simg):
            # simg will be empty string if not provided by the user
            if simg:
                try:
                    self.replace_arg(
                        target, self.params[target].format(simg)
                    )
                except KeyError:
                    Display.error(
                        what='Singularity Image for Cluster {0} '.format(self.__class__.__name__),
                        info=' [ Not Supported ]',
                        fill='-'
                    )
                    self.replace_arg(target, '')
            else:
                Display.error(
                    what='Singularity Image for Cluster {0} '.format(self.__class__.__name__),
                    info=' [ not provided ]',
                    fill='-'
                )
                self.replace_arg(target, '')

        def replace_varargs(self, target, items):
            values = []
            default = settings.DEFAULT_ARGS.get(target, [])
            if default == items:
                if default:
                    if len(default) > 1:
                        raise ValueError('Multiple Default values exist for {0}.'.format(target))
                    values.append(default[0])
            else:
                for item in items:
                    # Must check whether the requested resource is available for this Cluster
                    # TODO : On next Iteration
                    values.append(self.params[target].format(item))

            self.template = self.template.replace(
                target,
                '\n'.join(values)
            )

        def __store_run_script(self, *, nodes, np):
            output_path = os.path.join(
                self.benchmark_directory,
                'n-{0}-p-{1}'.format(nodes, np)
            )
            os.mkdir(output_path)
            run_file = os.path.join(
                output_path,
                settings.DEFAULT_SCRIPT_NAME
            )
            with open(run_file, 'w') as file:
                file.write(self.template)

        def __update_template(self):
            Display.title(
                title='Updating Template for {0}'.format(self.__class__.__name__)
            )
            templte_backup = self.template[:]
            for nnodes in range(self.args.min_nodes, self.args.max_nodes + 1, 1):
                for ntasks in range(self.args.min_ntasks_per_node, self.args.max_ntasks_per_node + 1, 1):
                    self.computed_params['$nodes$'] = str(nnodes)
                    self.computed_params['$ntasks-per-node$'] = str(ntasks)
                    self.computed_params['$MPI_NP$'] = str(nnodes * ntasks)

                    for (target, action) in self.targets.items():
                        try:
                            method = object.__getattribute__(self, action)
                        except AttributeError:
                            print('Class {0} does not have handler method named : {1}'.format(
                                self.__class__.__name__,
                                action
                            ))
                        else:
                            try:
                                Display.info(
                                    what='{0} Replaced by '.format(target),
                                    info=' [ {0} ]'.format(getattr(self.args, target[1:-1])),
                                    fill='-'
                                )
                                method(target, getattr(self.args, target[1:-1]))
                            except AttributeError:
                                Display.info(
                                    what='{0} Replaced by '.format(target),
                                    info=' [ {0} ]'.format(self.computed_params[target]),
                                    fill='-'
                                )
                                # print('Target {0} will be replaced with value computed from the user input'.format(target))
                                method(target, self.computed_params[target])

                    # write the script to the external file
                    self.__store_run_script(
                        nodes=self.computed_params['$nodes$'],
                        np=self.computed_params['$MPI_NP$']
                    )
                    # reload template for the next run
                    self.template = templte_backup[:]

    class PDC(ClusterMixin):
        OMP_NUM_THREADS = 'OMP_NUM_THREADS'
        ENABLE_THREADS = '$enable_threads$'
        params = {
            '$gres$': '#SBATCH --gres={0}',
            '$modules$': 'module load {0}',
            '$envs$': 'export {0}',
            '$memories$': '--mem={0}',
            '$threads$': 'export {0}={1}',
            '$enable_threads$': '-ntomp ${0} '
        }

        sbatch = 'sbatch'

        def __init__(self, *, args):
            ClusterMixin.__init__(self, args=args)

        def set_threads(self, target, value):
            if self.args.threads:
                self.replace_arg(target, self.params[target].format(self.OMP_NUM_THREADS, value))
                # settion
                self.replace_arg(self.ENABLE_THREADS, self.params[self.ENABLE_THREADS].format(self.OMP_NUM_THREADS))
            else:
                self.replace_arg(target, '')
                self.replace_arg(self.ENABLE_THREADS, '')

            # update the execute line

        @classmethod
        def inspect(cls):
            pipe = os.popen('squeue -u {0}'.format(os.environ['USER']))
            for line in pipe:
                Display.line(line)

        @classmethod
        def submit(cls, *, directory, job):
            current_working_directory = os.getcwd()
            os.chdir(directory)
            os.system('{0} {1}'.format(cls.sbatch, job))
            os.chdir(current_working_directory)
            Display.info(
                what='{0} '.format(os.path.join(directory, job)),
                info=' [ Submitted ]',
                fill='-'
            )

    class Tegner(PDC):
        def __init__(self, *, args):
            self.extend_super()
            PDC.__init__(self, args=args)

        def extend_super(self):
            self.params = PDC.params.copy()
            self.params.update(
                {
                    '$simg$': 'singularity exec -B /cfs/klemming {0}',
                }
            )

    class Beskow(PDC):
        def __init__(self, *, args):
            PDC.__init__(self, args=args)
