from aiohttp import web
from gino import Gino
import json


app = web.Application()
db = Gino()


class AdsModel(db.Model):
    __tablename__ = 'Ads'
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String)
    description = db.Column(db.String)
    create_date = db.Column(db.DateTime, server_default=db.func.now())
    owner = db.Column(db.String)

async def orm_context(app):
    await db.set_bind('postgresql://postgres:rossiyanka@127.0.0.1:5432/aiohttp')
    await db.gino.create_all()
    yield
    await db.pop_bind().close()

app.cleanup_ctx.append(orm_context)


class AdsView(web.View):

    async def get(self):
        advt = await AdsModel.get(int(self.request.match_info['id']))
        if advt is None:
            raise web.HTTPNotFound(content_type='application/json', text=json.dumps({
                'error': 'adtv not found '
            }))
        return web.json_response(
            {'header': advt.header}
        )


    async def post(self):
        request = self.request
        json_data = await request.json()
        new_advt = await AdsModel.create(**json_data)
        return web.json_response({
            'id': new_advt.id
        })

    async def delete(self):
        advt = await AdsModel.get(int(self.request.match_info['id']))
        if advt is None:
            raise web.HTTPNotFound(content_type='application/json', text=json.dumps({
                'error': 'adtv not found '
            }))
        await advt.delete()
        return web.json_response(
            {'header': advt.header}
        )



app.add_routes([
    web.post('/ads/', AdsView),
    web.get('/ads/{id}', AdsView),
    web.delete('/ads/{id}', AdsView), ])



web.run_app(app)