import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', help='Name of the ENVIRONMENT. ' +
                        'If ABSOLUTE PATH not given, CURRENT WORKING DIRECTORY will be appended.',
                        type=str, required=True)
    args = parser.parse_args()
    env_path = os.path.abspath(args.env)

    os.system(f'conda create --prefix {env_path} python=3.7 matplotlib=3.1 pandas=1.0.3 seaborn=0.10.1 --yes')

    print(f'Your Conda Environment has been created successfully here: {env_path}')

    print('You can Activate the Environment using the following command: \n' +
          f'\tconda activate {env_path}')
