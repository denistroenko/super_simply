def mapping_view(app: object):
    @app.route('/_ss')
    def shows_ss():
        return 'Super Simply'
