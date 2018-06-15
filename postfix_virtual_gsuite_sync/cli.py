from operator import itemgetter

import click
from googleapiclient.errors import HttpError
from oauth2client import client, file, tools

from postfix_virtual_gsuite_sync.alias_updater import SCOPES, AliasUpdater
from postfix_virtual_gsuite_sync.postfix_virtual import parse_virtual_file


@click.command()
@click.option(
    '--client-secret-file',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default='client_secret.json'
)
@click.option(
    '--credentials-file',
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    default='credentials.json'
)
@click.argument('target-domain')
@click.argument('virtual-file', type=click.File())
def main(client_secret_file, credentials_file, target_domain, virtual_file):
    store = file.Storage(credentials_file)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, SCOPES)
        creds = tools.run_flow(flow, store, flags=tools.argparser.parse_args([]))

    updater = AliasUpdater(creds)

    for target, should_aliases in sorted(
            parse_virtual_file(virtual_file, target_domain).items(),
            key=itemgetter(0)
    ):
        try:
            user = updater.users[target]
            if target in should_aliases:
                should_aliases.remove(target)
            existing_aliases = user.aliases
            click.secho(f'Processing {target}...', fg='blue', nl=False)
            if should_aliases != existing_aliases:
                print()
                aliases_to_add = should_aliases - existing_aliases
                if aliases_to_add:
                    click.secho('  Adding aliases:', fg='green')
                for alias_to_add in aliases_to_add:
                    user.add_alias(alias_to_add)
                    click.secho(f'  - {alias_to_add}', fg='green')
                aliases_to_del = existing_aliases - should_aliases
                if aliases_to_del:
                    click.secho('  Removing aliases:', fg='yellow')
                for alias_to_del in aliases_to_del:
                    user.delete_alias(alias_to_del)
                    click.secho(f'  - {alias_to_del}', fg='yellow')
            else:
                click.secho('ok', fg='green')
        except HttpError:
            click.secho(f'Error fetching {target}\n', fg='red')
            continue


if __name__ == "__main__":
    main()
