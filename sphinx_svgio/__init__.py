
def setup(app) -> dict:
    from .list import setup_svgio_list
    from .svgio import setup_svgio

    setup_svgio(app)
    setup_svgio_list(app)
    return {
        "version": "0.0.5",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
