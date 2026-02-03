import json
import os

def handler(event: dict, context) -> dict:
    """API для отслеживания активных сессий на сайте в реальном времени"""
    
    method = event.get('httpMethod', 'GET').upper()
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    try:
        import psycopg2
        
        dsn = os.environ['DATABASE_URL']
        conn = psycopg2.connect(dsn)
        conn.autocommit = True
        cur = conn.cursor()
        
        schema = 't_p20980907_session_widget_proje'
        
        if method == 'POST':
            body_str = event.get('body', '{}')
            if isinstance(body_str, str):
                body = json.loads(body_str)
            else:
                body = body_str
            
            if isinstance(body, dict):
                session_id = body.get('session_id')
            else:
                session_id = None
            
            if not session_id:
                conn.close()
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'session_id is required'}),
                    'isBase64Encoded': False
                }
            
            insert_query = f'''
                INSERT INTO {schema}.sessions (session_id, last_active, created_at)
                VALUES (%s, NOW(), NOW())
                ON CONFLICT (session_id)
                DO UPDATE SET last_active = NOW()
            '''
            cur.execute(insert_query, (session_id,))
            
            count_query = f'''
                SELECT COUNT(*) FROM {schema}.sessions
                WHERE last_active > NOW() - INTERVAL '5 minutes'
            '''
            cur.execute(count_query)
            active_count = cur.fetchone()[0]
            
            conn.close()
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'active_sessions': active_count,
                    'session_id': session_id
                }),
                'isBase64Encoded': False
            }
        
        elif method == 'GET':
            count_query = f'''
                SELECT COUNT(*) FROM {schema}.sessions
                WHERE last_active > NOW() - INTERVAL '5 minutes'
            '''
            cur.execute(count_query)
            active_count = cur.fetchone()[0]
            
            conn.close()
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'active_sessions': active_count
                }),
                'isBase64Encoded': False
            }
        
        conn.close()
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Method not allowed'}),
            'isBase64Encoded': False
        }
    
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\\n{traceback.format_exc()}"
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': error_detail}),
            'isBase64Encoded': False
        }