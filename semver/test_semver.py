import mock

from semver import SemanticVersioning


def test_default_prefix():
    semver = SemanticVersioning()
    assert semver.prefix == 'v'


def test_custom_prefix():
    semver = SemanticVersioning(prefix='foo')
    assert semver.prefix == 'foo'


def test_is_match_default_prefix():
    semver = SemanticVersioning()
    assert semver.is_match('v1.0.0')


def test_not_a_match_default_prefix():
    semver = SemanticVersioning()
    assert not semver.is_match('foo1.0.0')


def test_is_match_with_custom_prefix():
    semver = SemanticVersioning(prefix='vstaging')
    assert semver.is_match('vstaging1.0.0')


def test_not_a_match_with_custom_prefix():
    semver = SemanticVersioning(prefix='vstaging')
    assert not semver.is_match('foo1.0.0')


def test_next_version_default_behaviour():
    """default behaviour is to increment the minor version"""
    with mock.patch.object(SemanticVersioning, 'current', return_value='v1.0.0'):
        semver = SemanticVersioning()
        assert semver.next_version() == 'v1.1.0'


def test_next_major_version():
    """default behaviour is to increment the minor version"""
    with mock.patch.object(SemanticVersioning, 'current', return_value='v1.0.0'):
        semver = SemanticVersioning()
        assert semver.next_version(release_type='major') == 'v2.0.0'


def test_next_minor_version():
    """default behaviour is to increment the minor version"""
    with mock.patch.object(SemanticVersioning, 'current', return_value='v1.0.0'):
        semver = SemanticVersioning()
        assert semver.next_version(release_type='minor') == 'v1.1.0'


def test_next_patch_version():
    """default behaviour is to increment the minor version"""
    with mock.patch.object(SemanticVersioning, 'current', return_value='v1.0.0'):
        semver = SemanticVersioning()
        assert semver.next_version(release_type='patch') == 'v1.0.1'
