# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Tests for get command

"""

__docformat__ = 'restructuredtext'

from os.path import join as opj
from ...api import upgrade_handle

from ...support.annexrepo import AnnexRepo
from ...tests.utils import assert_raises, eq_
from ...tests.utils import with_testrepos
from ...tests.utils import assert_cwd_unchanged
from ...tests.utils import ok_startswith
from ...utils import rmtree


@assert_cwd_unchanged
@with_testrepos('.*handle.*', flavors=['clone'])
def test_upgrade_handle(path):
    repo = AnnexRepo(path, create=False, init=True)
    # it is there and needs to be initialized after cloning
    # TODO: that 'init' has to move to testrepo setup somehow

    upgrade_handle(path)  # shouldn't fail if nothing to upgrade

    # remove remote 'origin' -- should fail
    repo.git_remote_remove('origin')
    eq_(repo.git_get_remotes(), [])

    with assert_raises(RuntimeError) as ex:
        upgrade_handle(path)
    ok_startswith(str(ex.exception), 'No remotes were found for %s' % path)

    # remove .git altogether
    rmtree(opj(path, '.git'))
    with assert_raises(RuntimeError) as ex:
        upgrade_handle(path)
    ok_startswith(str(ex.exception), 'No handle repository found in %s' % path)


# TODO: test actual upgrade:
#  probably generate a clone of a clone,
#  update original clone,
#  verify that upgrade was carried out
