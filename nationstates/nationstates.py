try:
    import nationstates as ns
except:
    ns = None
import discord
from discord.ext import commands
from __main__ import send_cmd_help
from random import choice

class NationStates:

    def __init__(self, bot):
        self.bot = bot
        self.api = ns.Api('zephyrkul@outlook.com')

    @commands.command()
    async def nation(self, *, nation):
        """Retrieves info about a specified NationStates nation"""
        if nation[0] == nation[-1] and nation.startswith('"'):
            nation = nation[1:-1]
        try:
            data = self.api.get_nation(nation, ['id', 'category', 'flag', 'founded', 'freedom', 'fullname', 'influence', 'motto', 'population', 'region', 'wa', ns.Shard('census', scale='65+66', mode='score')]).collect()
        except ns.NScore.exceptions.NotFound:
            await self.bot.say('`Nation "%s" does not exist`' % nation)
            return
        regdata = self.api.get_region(data['region'], ['id', 'delegate', 'founder']).collect()
        foudel = ''
        if regdata['founder'] == data['id']:
            foudel = '(Founder) '
        if int(data['population']) >= 1000:
            data['population'] = '%s billion' % str(float(data['population']) / 1000)
        else:
            data['population'] += ' million'
        endo = float(data['census']['scale'][1]['score'])
        if endo == 1:
            endo = '%u endorsement' % endo
        else:
            endo = '%u endorsements' % endo
        if data['founded'] == '0':
            data['founded'] = 'in Antiquity'
        embed = discord.Embed(title=data['fullname'], url='https://www.nationstates.net/nation=%s'%data['id'], description='[%s](https://www.nationstates.net/region=%s) %s| %s | Founded %s'%(data['region'],regdata['id'],foudel,data['population'],data['founded']), colour=int(''.join([choice('0123456789ABCDEF') for x in range(6)]), 16))
        embed.set_author(name="NationStates", url='https://www.nationstates.net/')
        embed.set_thumbnail(url=data['flag'])
        embed.add_field(name=data['category'], value='%s | %s | %s\n\n*"%s"*\n\n%s | %s | %u influence (%s)'%(data['freedom']['civilrights'],data['freedom']['economy'],data['freedom']['politicalfreedom'],data['motto'],data['unstatus'],endo,float(data['census']['scale'][0]['score']),data['influence']), inline=False)
        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say('I need the `Embed links` permission to send this')

    @commands.command()
    async def region(self, *, region):
        """Retrieves info about a specified NationStates region"""
        if region[0] == region[-1] and region.startswith('"'):
            region = region[1:-1]
        try:
            data = self.api.get_region(region, ['delegate', 'delegateauth', 'flag', 'founded', 'founder', 'name', 'numnations', 'power']).collect()
        except ns.NScore.exceptions.NotFound:
            await self.bot.say('`Region "%s" does not exist`' % region)
            return
        if data['delegate'] == '0':
            data['delegate'] = 'No Delegate'
        else:
            deldata = self.api.get_nation(data['delegate'], ['fullname', 'influence', ns.Shard('census', scale='65+66', mode='score')])
            endo = float(deldata['census']['scale'][1]['score'])
            if endo == 1:
                endo = '%u endorsement' % endo
            else:
                endo = '%u endorsements' % endo
            data['delegate'] = '[%s](https://www.nationstates.net/nation=%s) | %s | %u influence (%s)' % (deldata['fullname'], data['delegate'], endo, float(deldata['census']['scale'][0]['score']), deldata['influence'])
        if 'X' in data['delegateauth']:
            data['delegateauth'] = ''
        else:
            data['delegateauth'] = ' (Non-Executive)'
        if data['founded'] == '0':
            data['founded'] = 'in Antiquity'
        if data['founder'] == '0':
            data['founder'] = 'No Founder'
        else:
            try:
                data['founder'] = '[%s](https://www.nationstates.net/nation=%s)' % (self.api.get_nation(data['founder'], ['fullname']).collect()['fullname'], data['founder'])
            except ns.NScore.exceptions.NotFound:
                data['founder'] += ' (Ceased to Exist)'
        embed = discord.Embed(title=data['name'], url='https://www.nationstates.net/region=%s'%(data['id']), description='[%s nations](https://www.nationstates.net/region=%s/page=list_nations) | Founded %s | Power: %s'%(data['numnations'],data['id'],data['founded'],data['power']), colour=int(''.join([choice('0123456789ABCDEF') for x in range(6)]), 16))
        embed.set_author(name="NationStates", url='https://www.nationstates.net/')
        if data['flag']:
            embed.set_thumbnail(url=data['flag'])
        embed.add_field(name='Founder', value=data['founder'], inline=False)
        embed.add_field(name='Delegate%s'%(data['delegateauth']), value=data['delegate'], inline=False)
        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say('I need the `Embed links` permission to send this')

def setup(bot):
    if ns is None:
        raise RuntimeError('You\'re missing the NationStates library.\nInstall it with "pip install nationstates" and reload the module.')
    bot.add_cog(NationStates(bot))
