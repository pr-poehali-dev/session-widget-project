import json
import os
import psycopg2

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
    
    conn = None
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        schema = os.environ.get('MAIN_DB_SCHEMA', 'public')
        cur.execute(f'SET search_path TO {schema}')
        
        if method == 'POST':
            body = json.loads(event.get('body', '{}'))
            session_id = body.get('session_id')
            
            if not session_id:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'session_id is required'}),
                    'isBase64Encoded': False
                }
            
            cur.execute('''
                INSERT INTO sessions (session_id, last_active, created_at)
                VALUES (%s, NOW(), NOW())
                ON CONFLICT (session_id)
                DO UPDATE SET last_active = NOW()
            ''', (session_id,))
            conn.commit()
            
            cur.execute('''
                SELECT COUNT(*) FROM sessions
                WHERE last_active > NOW() - INTERVAL '5 minutes'
            ''')
            active_count = cur.fetchone()[0]
            
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
            cur.execute('''
                SELECT COUNT(*) FROM sessions
                WHERE last_active > NOW() - INTERVAL '5 minutes'
            ''')
            active_count = cur.fetchone()[0]
            
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
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)}),
            'isBase64Encoded': False
        }
    finally:
        if conn:
            conn.close()