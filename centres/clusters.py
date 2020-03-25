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
        }

        def __init__(self, *, args):
            self.args = args

            #  housekeeping for storing job script
            self.__housekeeping()
            # load the template
            self.__load_template()
            # Replace target by the user provided value in the template
            self.__update_template()

        def __housekeeping(self):
            try:
                workdir = os.path.abspath(self.args.workdir)
            except Exception:
                raise Exception('No default or user provided Working directory was provided...')
            else:
                if workdir == settings.HOME_DIRECTORY:
                    print('Warning: Using program directory as working directory.')
                    confirmation = input("Type 'y/Y' to confirm? ")
                    if not confirmation in ['y', 'Y']:
                        print('Aborting Program...')
                        sys.exit()
                    if workdir != settings.DEFAULT_WORKDIR:
                        os.chdir(workdir)
                        print('Working directory set to : {0}'.format(workdir))
                    else:
                        print('Using the Directory {0} as working directory'.format(settings.DEFAULT_WORKDIR))
                else:
                    if workdir != settings.DEFAULT_WORKDIR:
                        os.chdir(workdir)
                        print('Working directory set to : {0}'.format(workdir))
                    else:
                        print('Using the default directory {0} as working directory'.format(settings.DEFAULT_WORKDIR))

            #  Creating Directory for the benchmark
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
                    confirmation = input("Warning : {0} Already exists. \
                        \n Type o/O' to override, 'b/b' for backup old result and any other key to quit.\n".format(
                        self.benchmark_directory)
                    )
                    if confirmation in ['o', 'O']:
                        # Remove every thing from the directory
                        print('Warning : Overriding {0}'.format(self.benchmark_directory))
                        os.system('rm -rf {0}'.format(
                            os.path.join(self.benchmark_directory, '*'))
                        )
                    elif confirmation in ['b', 'B']:
                        Display.title(title='BACKING UP CONTENTS OF: {0}'.format(self.benchmark_directory))
                        Display.info(what='DEFAULT BACKUP SUFFIX ', info=' [ "{0}" ]'.format(
                            settings.DEFAULT_FILE_BACKUP_SUFFIX)
                        )
                        # Storing current working directory
                        cwd = os.getcwd()
                        os.chdir(self.benchmark_directory)
                        for content in sorted(contents_here, reverse=True):
                            os.rename(content, content + settings.DEFAULT_FILE_BACKUP_SUFFIX)

                        # going back to the working directory as it was
                        os.chdir(cwd)

                    else:
                        print('Aborting Program...')
                        sys.exit()

        def __load_template(self):
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
                print('Template found for Cluster: {0}.'.format(
                    self.__class__.__name__
                ))

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
                    sys.stderr.write(
                        'Cluster {0} does not support Singularity Image.\n'.format(self.__class__.__name__)
                    )
                    self.replace_arg(target, '')
            else:
                sys.stdout.write(
                    'Cluster {0}: Singularity Image not provided.\n'.format(self.__class__.__name__)
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
                                method(target, getattr(self.args, target[1:-1]))
                            except AttributeError:
                                print('Target {0} will be replaced with value computed from the user input'.format(target))
                                method(target, self.computed_params[target])

                    # write the script to the external file
                    self.__store_run_script(
                        nodes=self.computed_params['$nodes$'],
                        np=self.computed_params['$MPI_NP$']
                    )
                    # reload template for the next run
                    self.__load_template()

    class PDC(ClusterMixin):
        params = {
            '$gres$': '#SBATCH --gres={0}',
            '$modules$': 'module load {0}',
            '$envs$': 'export {0}',
            '$memories$': '--mem={0}'
        }

        sbatch = 'sbatch'

        def __init__(self, *, args):
            ClusterMixin.__init__(self, args=args)

        @classmethod
        def submit(cls, *, directory, job):
            current_working_directory = os.getcwd()
            os.chdir(directory)
            os.system('{0} {1}'.format(cls.sbatch, job))
            os.chdir(current_working_directory)

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
