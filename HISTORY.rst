.. :changelog:

History
-------

0.0.1 (13-05-2020)
---------------------

* First code creation


0.1.0 (13-05-2020)
------------------

* first commit


0.1.1 (13-05-2020)
------------------

* pypi complains filename has been used, increment version


0.1.2 (13-05-2020)
------------------

* entry_point modified


0.1.3 (13-05-2020)
------------------

* program blows up when no config file is provided - fixed


0.1.4 (15-05-2020)
------------------

* bug fixed (connections would freeze after a few minutes) + else branches added + wrote few lines of code for debugging purposes


0.1.5 (15-05-2020)
------------------

* bug is really fixed now (connections would freeze after a few minutes)


0.1.6 (16-05-2020)
------------------

* cli refactored due to changes in API of lib: the constant GROUP_PORTS has to be passed to several classes and the new method named tunnel.periodically_purge_buffer() has to be invoked once
