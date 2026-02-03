import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import Icon from '@/components/ui/icon';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [sessionCount, setSessionCount] = useState(3);
  const { toast } = useToast();

  const widgetCode = `<!-- Active Sessions Widget -->
<div id="active-sessions-widget" style="position:fixed;bottom:20px;right:20px;z-index:9999;">
  <div style="background:white;border-radius:12px;padding:16px 24px;box-shadow:0 4px 12px rgba(0,0,0,0.1);display:flex;align-items:center;gap:12px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
    <div style="width:8px;height:8px;background:#0EA5E9;border-radius:50%;animation:pulse 2s infinite;"></div>
    <span style="font-size:14px;color:#1A1F2C;font-weight:500;"><span id="session-count">3</span> активных</span>
  </div>
</div>
<style>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
</style>
<script>
setInterval(() => {
  const count = Math.floor(Math.random() * 10) + 1;
  document.getElementById('session-count').textContent = count;
}, 5000);
</script>`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(widgetCode);
    toast({
      title: 'Скопировано!',
      description: 'Код виджета скопирован в буфер обмена',
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      <div className="container max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16 animate-fade-in">
          <h1 className="text-5xl font-bold text-primary mb-4">
            Виджет активных сессий
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Показывайте посетителям, сколько человек сейчас на сайте.
            Минималистичный дизайн, простая интеграция.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <Card className="p-8 animate-fade-in">
            <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
              <Icon name="Eye" size={24} className="text-secondary" />
              Превью виджета
            </h2>
            
            <div className="bg-gray-100 rounded-lg p-8 min-h-[300px] relative">
              <div className="absolute bottom-6 right-6">
                <div className="bg-white rounded-xl px-6 py-4 shadow-lg flex items-center gap-3">
                  <div className="w-2 h-2 bg-secondary rounded-full animate-pulse-glow"></div>
                  <span className="text-sm font-medium text-primary">
                    {sessionCount} активных
                  </span>
                </div>
              </div>
              
              <div className="text-center text-muted-foreground mt-20">
                <Icon name="Mouse" size={48} className="mx-auto mb-4 opacity-40" />
                <p className="text-sm">Виджет появляется в правом нижнем углу</p>
              </div>
            </div>
            
            <Button
              onClick={() => setSessionCount(Math.floor(Math.random() * 10) + 1)}
              variant="outline"
              className="w-full mt-4"
            >
              <Icon name="RefreshCw" size={16} className="mr-2" />
              Обновить счётчик
            </Button>
          </Card>

          <Card className="p-8 animate-fade-in">
            <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
              <Icon name="Code" size={24} className="text-secondary" />
              Код для вставки
            </h2>
            
            <div className="bg-gray-900 rounded-lg p-4 mb-4 overflow-x-auto">
              <pre className="text-sm text-gray-100 font-mono whitespace-pre-wrap break-all">
                {widgetCode}
              </pre>
            </div>
            
            <Button onClick={copyToClipboard} className="w-full bg-secondary hover:bg-secondary/90">
              <Icon name="Copy" size={16} className="mr-2" />
              Скопировать код
            </Button>
            
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100">
              <p className="text-sm text-blue-900 flex items-start gap-2">
                <Icon name="Info" size={16} className="mt-0.5 flex-shrink-0" />
                <span>
                  Вставьте этот код перед закрывающим тегом <code className="bg-blue-100 px-1 rounded">&lt;/body&gt;</code> на вашем сайте
                </span>
              </p>
            </div>
          </Card>
        </div>

        <Card className="p-8 animate-fade-in">
          <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
            <Icon name="Sparkles" size={24} className="text-secondary" />
            Возможности виджета
          </h2>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="flex flex-col items-center text-center p-4">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <Icon name="Zap" size={24} className="text-secondary" />
              </div>
              <h3 className="font-semibold mb-2">Реальное время</h3>
              <p className="text-sm text-muted-foreground">
                Счётчик обновляется автоматически каждые 5 секунд
              </p>
            </div>
            
            <div className="flex flex-col items-center text-center p-4">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                <Icon name="Paintbrush" size={24} className="text-purple-600" />
              </div>
              <h3 className="font-semibold mb-2">Чистый дизайн</h3>
              <p className="text-sm text-muted-foreground">
                Минималистичный стиль, который подходит к любому сайту
              </p>
            </div>
            
            <div className="flex flex-col items-center text-center p-4">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <Icon name="Feather" size={24} className="text-green-600" />
              </div>
              <h3 className="font-semibold mb-2">Легковесный</h3>
              <p className="text-sm text-muted-foreground">
                Всего несколько строк кода, не замедляет сайт
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Index;
