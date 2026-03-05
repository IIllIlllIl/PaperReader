#!/bin/bash

# PaperReader Skill 安装脚本
# 自动安装skill到Claude配置目录

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   PaperReader Skill 安装程序${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查Claude配置目录
CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_DIR/skills"

if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "${YELLOW}创建Claude配置目录...${NC}"
    mkdir -p "$CLAUDE_DIR"
    echo -e "${GREEN}✓ 已创建: $CLAUDE_DIR${NC}"
fi

if [ ! -d "$SKILLS_DIR" ]; then
    echo -e "${YELLOW}创建skills目录...${NC}"
    mkdir -p "$SKILLS_DIR"
    echo -e "${GREEN}✓ 已创建: $SKILLS_DIR${NC}"
fi

echo ""
echo -e "${BLUE}安装PaperReader skill...${NC}"
echo ""

# 复制YAML配置
if [ -f "$PROJECT_ROOT/skills/paper_reader.yaml" ]; then
    cp "$PROJECT_ROOT/skills/paper_reader.yaml" "$SKILLS_DIR/"
    echo -e "${GREEN}✓ 已安装: paper_reader.yaml${NC}"
else
    echo -e "${RED}✗ 错误: 找不到 paper_reader.yaml${NC}"
    exit 1
fi

# 复制Python处理器
if [ -f "$PROJECT_ROOT/skills/paper_reader.py" ]; then
    cp "$PROJECT_ROOT/skills/paper_reader.py" "$SKILLS_DIR/"
    echo -e "${GREEN}✓ 已安装: paper_reader.py${NC}"
else
    echo -e "${RED}✗ 错误: 找不到 paper_reader.py${NC}"
    exit 1
fi

# 检查依赖
echo ""
echo -e "${BLUE}检查依赖...${NC}"
echo ""

# 检查Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python已安装: $PYTHON_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Python3 未找到，请先安装Python 3.8+${NC}"
fi

# 检查pip依赖
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    echo -e "${YELLOW}检查Python依赖...${NC}"
    if python3 -c "import anthropic" 2>/dev/null; then
        echo -e "${GREEN}✓ anthropic 已安装${NC}"
    else
        echo -e "${YELLOW}⚠ anthropic 未安装${NC}"
        echo -e "${YELLOW}  运行: pip install -r requirements.txt${NC}"
    fi
else
    echo -e "${YELLOW}⚠ requirements.txt 未找到${NC}"
fi

# 检查Marp CLI
if command -v marp &> /dev/null; then
    MARP_VERSION=$(marp --version | head -1)
    echo -e "${GREEN}✓ Marp CLI已安装: $MARP_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Marp CLI 未找到${NC}"
    echo -e "${YELLOW}  安装: npm install -g @marp-team/marp-cli${NC}"
    echo -e "${YELLOW}  或者使用Markdown格式: /paper file.pdf --md${NC}"
fi

# 检查API密钥
echo ""
echo -e "${BLUE}检查配置...${NC}"
echo ""

if [ -f "$PROJECT_ROOT/.env" ]; then
    if grep -q "ANTHROPIC_API_KEY" "$PROJECT_ROOT/.env"; then
        echo -e "${GREEN}✓ API密钥已配置${NC}"
    else
        echo -e "${YELLOW}⚠ .env文件中未找到ANTHROPIC_API_KEY${NC}"
        echo -e "${YELLOW}  请编辑 .env 文件并添加您的API密钥${NC}"
    fi
else
    echo -e "${YELLOW}⚠ .env文件未找到${NC}"
    if [ -f "$PROJECT_ROOT/.env.example" ]; then
        echo -e "${YELLOW}  创建 .env 文件...${NC}"
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        echo -e "${GREEN}✓ 已创建 .env 文件${NC}"
        echo -e "${YELLOW}  请编辑 .env 并添加您的 ANTHROPIC_API_KEY${NC}"
    fi
fi

# 创建必要的目录
echo ""
echo -e "${BLUE}创建项目目录...${NC}"
echo ""

mkdir -p "$PROJECT_ROOT/papers"
mkdir -p "$PROJECT_ROOT/output/markdown"
mkdir -p "$PROJECT_ROOT/output/slides"
mkdir -p "$PROJECT_ROOT/cache"
mkdir -p "$PROJECT_ROOT/logs"

echo -e "${GREEN}✓ 目录结构已创建${NC}"

# 安装完成
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   ✅ 安装完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}下一步:${NC}"
echo ""
echo -e "1. ${YELLOW}配置API密钥${NC}（如果还没有）:"
echo -e "   ${BLUE}编辑 $PROJECT_ROOT/.env${NC}"
echo -e "   ${BLUE}添加: ANTHROPIC_API_KEY=your-key-here${NC}"
echo ""
echo -e "2. ${YELLOW}放置PDF论文${NC}:"
echo -e "   ${BLUE}cp /path/to/paper.pdf papers/${NC}"
echo ""
echo -e "3. ${YELLOW}在Claude对话框中使用${NC}:"
echo -e "   ${BLUE}/paper${NC}           ${GREEN}# 处理最新PDF${NC}"
echo -e "   ${BLUE}/paper file.pdf${NC}  ${GREEN}# 处理指定文件${NC}"
echo -e "   ${BLUE}/papers${NC}          ${GREEN}# 批量处理${NC}"
echo ""
echo -e "4. ${YELLOW}查看帮助${NC}:"
echo -e "   ${BLUE}cat skills/README.md${NC}"
echo ""
echo -e "${BLUE}快速测试:${NC}"
echo -e "   ${YELLOW}python3 -c \"from skills.paper_reader import handle_paper_command; print('✓ Skill已就绪')\"${NC}"
echo ""
echo -e "${GREEN}Happy reading! 📚${NC}"
